A) TERRAIN
	1. Create base terrain map via fractal perlin noise (mild)
	2. Generate tectonic plates via Worley noise: spread N plate-centers randomly
	3. Assign each tectonic plate a type: continental / oceanic
	4. Assign motion vector for each tectonic plate
	5. Initialize a neutral custom region_map for each special landform type (tectonic bias, mountain range, volcanic arc, trench, rift, etc. maps) (def: False)
	6. Initialize a neutral custom mask_noise map for each special landform type (def: 0)
	7. Create base/reference noise maps for each landform type
	8. Iterate over each cell in the map
	
	9. For each non-boundary cell:
		I. Apply Initial tectonic type-based elevation bias in the dedicated mask 
		
	10. For each boundary cell:
		I. Mark region cells based on interaction type in the appropriate region_map
		II. Convergent:
				- Continental-Continental: Centered "normal" mountain range
				- Continental-Oceanic: Centered trench + volcanic mountain arc, parallel to boundary, offset 100-300km into the continental plate
				- Oceanic-Oceanic: Centered trench + volcanic mountain arc, parallel to boundary, offset 100-300km into random plate of the two
			Divergent: 
				- Continental-Continental: Centered rifts
				- Continental-Oceanic: (SKIP)
				- Oceanic-Oceanic: Centered ridge
		III. In order to define an entire special region, for each boundary cell mark neighboring pixels for width
		
	11. For each cell in each region_map:
		I. Reference noise value for current cell by type, assign the value in mask_noise
	
	12. Smoothen all mask noises using box blur, appropriate blur strength individually
	13. Add all mask noises map over the terrain, combine them and re-normalize
	14. Set sea-level dynamically
	
	
B) TEMPERATURE
	1. Generate cosinusoidal, latitudal base temperature map (polars cold, equator hot)
	2. Reduce temperature based on elevation and lapse_rate ( ~6.5°C per 1000 meters )
	3. Add noise
	
	
C) Pericipitation (by iterative moisture simulation)
	1. Generate moisture map:
		I. Moist above ocean (elevation < sea_level)
		II. Add noise
		
	2. Generate prevailing winds vector field
	3. Run iterative moisture simulation (for each cell):
		I. 	Solve for a saturation threshold based on orographic lift (positive slope above water = lower saturation) and local temperature (lower temperature = lower saturation)
		II. If moisture > saturation, deduct moisture into percipitation by releaseFactor
		III. Move the moisture based on the prevailing winds
		IV. Retain some portion of the moisture in the current location, move the rest into the next position
	
	
D) Biome classification
	1. Determine the biome at each cell based on the biome map via the 3 factors ( Elevation, Temperature, Percipiation ) 