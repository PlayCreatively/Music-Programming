import json
import numpy as np
import hashlib
from pythonosc import udp_client
import state as S

# =============================================================================
# 1. SHARED SCHEMA CONFIGURATION
# =============================================================================
# These constants ensure the Loader and the OSC Sender always agree on the data layout.

# Global Scalar Keys (Order matters!)
GLOBAL_KEYS = [
    "transpose", "lfo_speed", "lfo_delay", 
    "pitch_mod_depth", "amp_mod_depth"
]

# Operator Scalar Keys (Order matters!)
# Note: 'output_level' is excluded here because it is baked into the Matrix/Envelopes in the parser
OP_SCALAR_KEYS = [
    "frequency_ratio_mode", "frequency_fixed_mode", 
    "detune"
]

# Calculated Sizes
SIZE_GLOBALS   = len(GLOBAL_KEYS)
SIZE_MATRIX    = 36
SIZE_MIXER     = 6
SIZE_PEG       = 4
# Per Operator: Scalars + 4 Rates + 4 Levels
SIZE_OP_PARAMS = len(OP_SCALAR_KEYS) + 4 + 4 

# Offsets for slicing the flat vector
OFFSET_GLOBALS = 0
OFFSET_MATRIX  = OFFSET_GLOBALS + SIZE_GLOBALS
OFFSET_MIXER   = OFFSET_MATRIX + SIZE_MATRIX
OFFSET_PEG     = OFFSET_MIXER + SIZE_MIXER
OFFSET_OPS     = OFFSET_PEG + SIZE_PEG

# =============================================================================
# 2. LOADER LOGIC
# =============================================================================

DEFAULT_DX7_SPEC = {
  "global": {
    "transpose": { "range": [-24, 24] },
    "lfo_speed": { "range": [0.06, 50.0] },
    "lfo_delay": { "range": [0.0, 3.0] },
    "pitch_mod_depth": { "range": [0, 99] },
    "amp_mod_depth": { "range": [0, 42] },
    "pitch_eg_levels": { "range": [-48, 48] },
    "wiring": { "range": [0.0, 12.57] } # [0..4pi]
  },
  "operator": {
    "ratio_mode": { "range": [0, 1] }, # lerps between fixed/ratio
    "frequency_ratio_mode": { "range": [0.5, 61.69] },
    "frequency_fixed_mode": { "range": [1, 9772] },
    "detune": { "range": [-20, 20] },
    "envelope": [
      { "rate": { "range": [0, 99] }, "level": { "range": [0, 12] } }
    ]
  }
}

def parse_range(r_arr):
    return float(r_arr[0]), float(r_arr[1])

def get_color_from_name(name):
    hash_val = int(hashlib.sha256(name.encode('utf-8')).hexdigest(), 16)
    r = (hash_val & 0xFF)
    g = ((hash_val >> 8) & 0xFF)
    b = ((hash_val >> 16) & 0xFF)
    return ((r + 255) // 2, (g + 255) // 2, (b + 255) // 2)

def load_dx7_json(file_path):
    """Parses JSON and populates state.py using the Shared Schema."""
    with open(file_path, 'r') as f:
        data = json.load(f)

    spec = data.get("dx7_parameter_spec", DEFAULT_DX7_SPEC)
    glob_spec = spec.get("global", DEFAULT_DX7_SPEC["global"])
    op_spec = spec.get("operator", DEFAULT_DX7_SPEC["operator"])

    dims = []
    mins = []
    maxs = []

    # 1. Global Scalars
    for k in GLOBAL_KEYS:
        range_data = glob_spec.get(k, DEFAULT_DX7_SPEC["global"].get(k))
        if range_data:
            dims.append(k)
            rmin, rmax = parse_range(range_data["range"])
            mins.append(rmin)
            maxs.append(rmax)

    # 2. Matrix
    wiring_spec = glob_spec.get("wiring", DEFAULT_DX7_SPEC["global"]["wiring"])
    w_min, w_max = parse_range(wiring_spec["range"])
    for i in range(SIZE_MATRIX):
        dims.append(f"wiring_{i}")
        mins.append(w_min); maxs.append(w_max)

    # 3. Mixer
    for i in range(SIZE_MIXER):
        dims.append(f"out_mix_{i}")
        mins.append(0.0); maxs.append(1.0)

    # 4. PEG
    range_data = glob_spec.get("pitch_eg_levels", DEFAULT_DX7_SPEC["global"]["pitch_eg_levels"])
    rmin, rmax = parse_range(range_data["range"])
    for i in range(SIZE_PEG):
        dims.append(f"pitch_eg_level_{i+1}")
        mins.append(rmin); maxs.append(rmax)

    # 5. Operators (6 down to 1)
    for op_id in range(6, 0, -1):
        prefix = f"op{op_id}"
        
        # Scalars
        for k in OP_SCALAR_KEYS:
            range_data = op_spec.get(k, DEFAULT_DX7_SPEC["operator"].get(k))
            if range_data:
                dims.append(f"{prefix}_{k}")
                rmin, rmax = parse_range(range_data["range"])
                mins.append(rmin); maxs.append(rmax)
        
        # Envelopes
        env_spec = op_spec.get("envelope", DEFAULT_DX7_SPEC["operator"]["envelope"])
        if env_spec:
            r_min, r_max = parse_range(env_spec[0]["rate"]["range"])
            l_min, l_max = parse_range(env_spec[0]["level"]["range"])
            for stage in range(1, 5):
                dims.append(f"{prefix}_eg_rate_{stage}")
                mins.append(r_min); maxs.append(r_max)
                dims.append(f"{prefix}_eg_level_{stage}")
                mins.append(l_min); maxs.append(l_max)

    # Init State
    print(f"Initializing Space with {len(dims)} dimensions...")
    S.init_space(dims)
    S.mins = np.array(mins, dtype=float)
    S.maxs = np.array(maxs, dtype=float)

    # Parse Vectors
    for p in data.get("patches", []):
        vector = []
        p_glob = p.get("global", {})
        p_ops = p.get("operators", [])
        p_name = p.get("identity", {}).get("name", "Unknown")

        # Global
        for k in GLOBAL_KEYS:
            val = p_glob.get(k, S.mins[dims.index(k)] if k in dims else 0.0)
            vector.append(float(val))

        vector.extend([float(x) for x in p_glob.get("algorithm_matrix", [0.0]*SIZE_MATRIX)])
        vector.extend([float(x) for x in p_glob.get("output_mixer", [0.0]*SIZE_MIXER)])
        vector.extend([float(x) for x in p_glob.get("pitch_eg_levels", [0.0]*SIZE_PEG)])

        # Operators
        op_map = {op['id']: op for op in p_ops}
        for op_id in range(6, 0, -1):
            curr_op = op_map.get(op_id, {})
            
            for k in OP_SCALAR_KEYS:
                val = curr_op.get(k)
                if val is None:
                    dim_name = f"op{op_id}_{k}"
                    val = S.mins[dims.index(dim_name)] if dim_name in dims else 0.0
                vector.append(float(val))

            env_list = curr_op.get("envelope", [])
            env_list.sort(key=lambda x: x['stage'])
            for stage_data in env_list:
                vector.append(float(stage_data['rate']))
                vector.append(float(stage_data['level']))

        col_tuple = get_color_from_name(p_name)

        # Validate bounds before adding
        v_arr = np.array(vector)
        # Use a small epsilon for floating point comparisons
        violations = np.where((v_arr < S.mins - 1e-5) | (v_arr > S.maxs + 1e-5))[0]
        if len(violations) > 0:
            idx = violations[0]
            param = S.param_names[idx]
            val = v_arr[idx]
            mn, mx = S.mins[idx], S.maxs[idx]
            raise AssertionError(f"Preset '{p_name}' param '{param}' value {val} is out of bounds [{mn}, {mx}]")

        S.add_preset(p_name, color=col_tuple, value=np.array([vector]))
    
    print(f"Loaded {len(S.preset_names)} presets.")


# =============================================================================
# 3. OSC CLIENT LOGIC
# =============================================================================

class DX7OSCClient:
    def __init__(self, ip="127.0.0.1", port=57120):
        self.client = udp_client.SimpleUDPClient(ip, port)
        
    def send_active_preset(self, active_vector: np.ndarray):
        """
        Unpacks the vector using the CONSTANTS defined above.
        Safe against schema changes as long as constants are updated.
        """
        data = active_vector.flatten().tolist()
        
        # --- 1. Slice using Shared Offsets ---
        # Note: Globals are indices 0 to OFFSET_MATRIX
        # We don't necessarily send globals to SC unless needed (e.g. LFO)
        
        wiring_matrix = data[OFFSET_MATRIX : OFFSET_MATRIX + SIZE_MATRIX]
        output_mixer  = data[OFFSET_MIXER  : OFFSET_MIXER + SIZE_MIXER]

        # --- 3. Unpack Operators ---
        op_ratios = []
        op_detunes = []
        op_env_times = []
        op_env_levels = []
        
        # We iterate 6 times. The data is stored [Op6, Op5 ... Op1]
        start_ptr = OFFSET_OPS
        
        for i in range(6):
            chunk = data[start_ptr : start_ptr + SIZE_OP_PARAMS]
            start_ptr += SIZE_OP_PARAMS
            
            # Map based on OP_SCALAR_KEYS order:
            # [0:Ratio, 1:Fixed, 2:Detune] -> Envelopes start at index 3
            
            op_ratios.append(chunk[0]) 
            op_detunes.append(chunk[2])
            
            # Envelope Extraction
            # Indices: Rate=3,5,7,9 | Level=4,6,8,10
            times = [chunk[3], chunk[5], chunk[7], chunk[9]]
            levels = [chunk[4], chunk[6], chunk[8], chunk[10]]
            
            op_env_times.append(times)
            op_env_levels.append(levels)

        # --- 4. Reorder for SuperCollider ---
        # Python: Op6 -> Op1
        # SC:     Op1 -> Op6
        op_ratios.reverse()
        op_detunes.reverse()
        op_env_times.reverse()
        op_env_levels.reverse()
        
        # Flatten lists for OSC
        flat_times = [t for op in op_env_times for t in op]
        flat_levels = [l for op in op_env_levels for l in op]

        # --- 5. Send ---
        # print(f"Sending OSC to {self.client._address}:{self.client._port}")
        self.client.send_message("/update_synth", [
            "opWiringMatrix", *wiring_matrix,
            "opOutMixer", *output_mixer,
            "opRatios", *op_ratios,
            "opEnvLevels", *flat_levels,
            "opEnvTimes", *flat_times
        ])
        
    def send_gate(self, is_on: bool):
        """Sends Note On (1) or Note Off (0)"""
        val = 1.0 if is_on else 0.0
        self.client.send_message("/gate", val)