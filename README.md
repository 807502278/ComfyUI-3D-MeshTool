# ComfyUI-3D-MeshTool

**Introduction**:
A simple 3D model processing tool within ComfyUI

**Partially referenced from everyone's plugins, if there is any inconvenience, please leave a message, and I will promptly remove the corresponding code.
For new features or suggestions, please provide feedback.**

**Update**:
2024-0705：
- `3d_meshtool`
    - `Array`  # Arrays can perform batch operations on certain properties, such as the of zero123, image batches, creating certain increments, etc.
        - `basics`  # Create an array
            - `array1 step`  # Generate an array with a starting value and step size.
            - `array1 end increment`  # Generate an array with a starting value, end value, and increment.
            - `array1 end step`  # Generate an array with a starting value, end value, and step size.
            - `array1 step increment`  # Generate an array with a starting value, step size, and increment.
            - `string to array`  # Convert a string to an array, including standardized brackets/removing non-numeric functions.
        - `calculation`
            - `array1 T`  # Transpose the array
            - `array1 number to angle`  # Convert array numbers to angles, including semi-angles.
            - `array1 append`  # Concatenate arrays, automatically determining 1D and 2D addition.
            - `array1 is null`  # Check if the array is empty.
            - `array1 attribute`  # Retrieve array attributes.
            - `array1 convert`  # Convert data types within the array.
            - `array1 select element`  # Select array elements, including standardized brackets/removing non-numeric functions.
    - `Basics`
        - `load_obj`  # Load an OBJ file.
        - `mesh_data`  # Retrieve mesh data.
        - `mesh_data_statistics`  # Statistics of mesh data, other than vertices and faces, other data is used to determine if it is empty.
        - `mesh_clean_data`  # Clean mesh data, can customize the removal of invalid or mismatched data.
    - `Camera`
        - `array1 to camposes`  # Convert an array to 3dpack camera poses (requires a 6xNx3 array, refer to 3dpack's campos standard).
    - `Edit`
        - `unwrapUV_xatlas`  # Latest (2023) UV unwrapping algorithm.
        - `UV_options`  # Settings for the unwrapUV_xatlas node, if not connected, default settings are used.
        - `Auto_Normal`  # Automatically calculate model normals.
    - `Optimization`
        - `mesh_optimization`  # Mesh optimization, select optimization types and parameters.
        - `mesh_cleanup`  # Mesh cleanup, select cleaning up model debris.
        - `mesh_subdivide`  # Mesh subdivision, increases vertices without changing the shape.
    - `Show`

**Roadmap**:
- `Basic Functions`
    - ✅ `Array sequence` (still needs optimization)
    - ✅ `Data conversion` (may need to add other conversions)
    - ✅ `OBJ import` (used code from 3dpack, still need to add whether the model is normalized and its data output to retain the original size and position when processing models in batch)
    - 🟩 `Simple direct preview window` (no need to save first) + preview window for world normals/depth/mask/specified view (can be used for compositing)
    - 🟩 `Save`, choose which data to save
- `Model Optimization`
    - ✅ `Remove debris`
    - ✅ `Reduce faces by percentage (vertices)`
    - ✅ `Cut subdivision`
    - 🟩 `Turbine smoothing`
    - 🟩 `Convert to quads`
    - 🟩... (other optimizations)
- `Model Editing`
    - ✅ `UV decomposition (xatlas)`
    - ✅ `Automatic vertex normals`
    - 🟩 `UV remap`
    - 🟩 `Restore normalized vertices to their original state`
    - 🟩 `High-poly to low-poly texture/bump baking, AO baking` (attempt to convert Blender's code to Comfyui)
    - 🟩... (other edits)
- `other`
    - 🟩 `Display any data.`
    - 🟩 `Example workflow`
