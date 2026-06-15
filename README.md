# Photobooth Filter Fix

## Problem
The original code only applied CSS filters visually to the video/image display. When capturing photos, `canvas.toDataURL()` saved the raw video frame without any filters applied.

## Solution
The updated code now applies filters directly to the canvas pixel data before saving:

### Key Changes in `photobooth_fixed.html`:

1. **Added `applyCanvasFilter()` function** - Manipulates pixel data for:
   - Grayscale: Averages RGB values
   - Sepia: Applies sepia tone matrix transformation
   - Invert: Inverts RGB values (255 - value)
   - Saturate: Increases color saturation by 220% with contrast boost

2. **Added `applyBlur()` function** - Implements box blur algorithm:
   - 3-pixel radius blur
   - Averages neighboring pixels for smooth effect

3. **Modified capture button handler** - Now calls filter functions after drawing to canvas:
   ```javascript
   // Draw mirrored video frame
   c.drawImage(v,0,0,cv.width,cv.height);
   
   // Apply filter to canvas BEFORE toDataURL()
   if(filter !== 'none') {
     if(filter === 'blur') {
       applyBlur(c);
     } else {
       applyCanvasFilter(c, filter);
     }
   }
   
   photo=cv.toDataURL(); // Now captures filtered image
   ```

4. **Removed CSS filter from preview** - Preview now shows the actual saved image (no CSS class needed)

## How It Works

1. User selects a filter (CSS still shows preview on video)
2. When "Capture" is clicked:
   - Video frame is drawn to canvas (mirrored)
   - Selected filter is applied to canvas pixel data
   - Canvas is converted to Base64 PNG
3. The saved photo now contains the actual filtered pixels

## Installation

1. Create folder structure:
   ```
   photobooth/
   ├── app.py (use app_photobooth.py)
   ├── templates/
   │   └── photobooth.html (use photobooth_fixed.html)
   └── static/
       └── photobooth.css (use your existing CSS)
   ```

2. Run the application:
   ```bash
   python app.py
   ```

3. Open browser to `http://localhost:5000`

## Technical Details

- **Grayscale**: Converts to average of R, G, B channels
- **Sepia**: Uses standard sepia matrix coefficients
- **Invert**: Subtracts each channel from 255
- **Blur**: Box blur with 3-pixel radius
- **Saturate**: Increases saturation by 2.2x and contrast by 1.5x

All filters are applied using pixel manipulation via `getImageData()` and `putImageData()`.