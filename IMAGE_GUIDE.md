# Image Guide - Adding Your Own Images

This guide explains how to replace the placeholder images with your own images.

## Current Image Setup

The website currently uses Unsplash images (free, high-quality stock photos). To use your own images:

## Option 1: Use Local Images (Recommended for Production)

### Step 1: Add Images to Project

1. Create an `images` folder in the `frontend` directory (if it doesn't exist):
   ```
   frontend/
   └── images/
   ```

2. Add your images to the `frontend/images/` folder:
   ```
   frontend/images/
   ├── about-building.jpg
   ├── project1.jpg
   ├── project2.jpg
   ├── project3.jpg
   ├── project4.jpg
   ├── project5.jpg
   ├── project6.jpg
   ├── interior1.jpg
   ├── interior2.jpg
   ├── interior3.jpg
   └── interior4.jpg
   ```

### Step 2: Update HTML File

Replace the image URLs in `frontend/index.html`:

**About Section:**
```html
<img src="images/about-building.jpg" 
     alt="Modern Architecture Building" 
     class="about-img">
```

**Projects Section (Project 1):**
```html
<img src="images/project1.jpg" 
     alt="Modern Villa Residence" 
     class="project-img">
```

**Interiors Section (Interior 1):**
```html
<img src="images/interior1.jpg" 
     alt="Modern Living Room Interior" 
     class="gallery-img">
```

### Step 3: Image Specifications

For best results, use these dimensions:

- **About Image**: 800x600px or larger (aspect ratio 4:3)
- **Project Images**: 600x400px or larger (aspect ratio 3:2)
- **Interior Images**: 500x400px or larger (aspect ratio 5:4)

**Recommended Formats:**
- JPG (for photos with many colors)
- WebP (for better compression)
- PNG (for images with transparency)

**File Size:** Keep images under 500KB each for faster loading.

---

## Option 2: Continue Using Unsplash Images

If you want to change Unsplash images but keep using their service:

1. Go to [Unsplash.com](https://unsplash.com)
2. Search for images (e.g., "modern architecture", "interior design")
3. Copy the image URL
4. Replace in HTML: `src="YOUR_UNSPLASH_URL"`

**Note:** Unsplash URLs are public and don't require authentication.

---

## Option 3: Use Other Image Hosting Services

You can use:
- **Cloudinary**: Free tier available
- **Imgur**: Free image hosting
- **AWS S3**: Your own storage (already in your stack)

---

## Image Optimization Tips

1. **Compress Images**: Use tools like:
   - [TinyPNG](https://tinypng.com)
   - [Squoosh](https://squoosh.app)
   - [ImageOptim](https://imageoptim.com)

2. **Use Modern Formats**: 
   - WebP format is 25-35% smaller than JPG
   - Modern browsers support it

3. **Lazy Loading**: 
   - Images already have lazy loading via CSS
   - Consider adding `loading="lazy"` attribute for better performance

---

## Example: Complete Image Update

Here's how to update all images at once:

**In `frontend/index.html`, replace:**

```html
<!-- About Section -->
<img src="https://images.unsplash.com/photo-1487958449943-2429e8be8625?w=800&h=600&fit=crop&auto=format" 
     alt="Modern Architecture Building" 
     class="about-img">
```

**With:**
```html
<img src="images/about-building.jpg" 
     alt="Modern Architecture Building" 
     class="about-img">
```

---

## Testing After Adding Images

1. **Start Local Server:**
   ```bash
   cd frontend
   python -m http.server 8000
   ```

2. **Check Browser Console (F12)** for any 404 errors on images

3. **Verify Images Load:**
   - Check Network tab in DevTools
   - All images should show status 200

---

## Troubleshooting

**Issue: Images don't display**
- Check file paths are correct (relative to HTML file)
- Verify image files exist in `frontend/images/` folder
- Check browser console for 404 errors

**Issue: Images are too large/slow**
- Compress images using tools mentioned above
- Use WebP format if possible
- Consider using image CDN

**Issue: Images look stretched/distorted**
- Ensure aspect ratios match recommendations
- Use `object-fit: cover` in CSS (already applied)
- Crop images to correct dimensions before uploading

---

## Quick Reference: Image Files Needed

| Location | Image File | Dimensions | Aspect Ratio |
|----------|------------|------------|--------------|
| About Section | `about-building.jpg` | 800x600px | 4:3 |
| Project 1 | `project1.jpg` | 600x400px | 3:2 |
| Project 2 | `project2.jpg` | 600x400px | 3:2 |
| Project 3 | `project3.jpg` | 600x400px | 3:2 |
| Project 4 | `project4.jpg` | 600x400px | 3:2 |
| Project 5 | `project5.jpg` | 600x400px | 3:2 |
| Project 6 | `project6.jpg` | 600x400px | 3:2 |
| Interior 1 | `interior1.jpg` | 500x400px | 5:4 |
| Interior 2 | `interior2.jpg` | 500x400px | 5:4 |
| Interior 3 | `interior3.jpg` | 500x400px | 5:4 |
| Interior 4 | `interior4.jpg` | 500x400px | 5:4 |

---

**Note:** The current setup uses Unsplash URLs which work immediately. To use local images, simply replace the `src` attributes in `index.html` with your local file paths.

