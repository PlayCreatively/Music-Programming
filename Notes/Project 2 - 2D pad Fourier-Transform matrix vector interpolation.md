vector representation of a Fourier Transform, getting 3 of quality SFX allows me to cross product it to make a 2D track pad to visually move around and between the 3 points 

- these points can be interpellated between using a b-spline
- to easily move all of the axis values slightly off to explore the neighbor areas is by applying small orbital rotation of the vector
- to add interactivity and natural physicality to this we can have a vector be stuck in a position and when force is applied on it it wiggles around like a spring, finally resting at the given spot

In theory I should be able to reconstruct the change of frequencies that represents an audio clip by plotting vector points featuring the frequency spectrum at that moment. Creating enough data points along t and then b-spline interpolate through those points should in theory reproduce the sound, allowing for saving an audios change or evolution over time as well as exploring neighboring sounds.


# multi-parameter latent space exploration
Having a beastly size synth with tens of parameters allows for a vast space of exploration. But sometimes it's hard to explore that space, especially when you don't understand what the knobs do. A tool that allows you to turn the knobs, save presets, plot multiple presets to a 2D plane that can be intuitively explored, to save more presets, from which new projections become possible.

## Ways of such projections:

> [!IDEA] ###  2D plane from 3 data points.
> Simply using the cross product.

 > [!IDEA] ### 2D plane from 4 data points, forming a rectangle from 2 polygons.
 > Having it morph between points would help with the folding of the two polygons, forming something closer to a taco
 
 > [!IDEA] ### 1D line interpolating through all the data points using B-Spline (ISSUE, READ BELOW)
 > To add the second dimension we can build a flat plane along the spline (like a road) but the issue is deciding their angles in order to lessen the screws.
 > 
 > ISSUE: The problem with the B-Spline is that we need to figure out which path to take (the order of data points) which is literally the [Traveling Salesman Problem](https://en.wikipedia.org/wiki/Travelling_salesman_problem) (not an easy problem). But Principal Curve (similar to PCA, except it trades linearity for data fitting accuracy) is an algorithm that does its best to approximate the path to take whilst preserving continuity, smooth curves and shortest distance.
 >  
 > ![[animation-1.webp|300]] ![[1570367893.gif|300]]
 > 
 > Principal Manifold is the general name for this which is a more generic term for fitting a M dimensional manifold onto N dimensional data points in N dimensional space.
 > Principal Plane is the term for fitting a 2D plane.
 > 
 > What just dawned at me as I look at the gifs above is that the algorithm seems to do a lot of *approximation* and overly trades fitting accuracy for distance. Since this algorithm is used in Machine Learning to train their models on training data which uses notorious amounts of dimensions as well as layers, the lazy fitting makes a lot of sense; but it does not match with my purposes as I'll be dealing with relatively few dimensions as well as pretty few "favorite" data points. So brute forcing to find the shortest path and interpolating using a B-Spline is the optimal path forward.
 
 
 
  > [!IDEA] ### 2D plane from PCA mapping from multiple data points
  > \- Negatives: 
  >  - it doesn't map onto the data points, it just gets close to them on average.
  >  
  > \+ Positives: 
  > + Might surface meaningful meta parameters that control multiple parameters.

> [!NOTE] Interesting thought
> Probably in theory, a combination of variables could map out all possible sounds and by using gradient descent map out any sound onto that space, therefore need to ensure a linear space to explore any and all sound 🤷

# Editor
To make it easy to quickly wire up all the parameters, it might be optimal to create a function that allows you to select multiple input parameters and right clip to create a vector node that connects to all of them. Then that vector node can be connected to the 2d pad node
