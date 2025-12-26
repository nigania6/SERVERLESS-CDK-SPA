# Local Testing Guide

This guide will help you test your SPA locally before deploying to AWS.

## 🚀 Quick Start

### Step 1: Test Frontend Locally

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Start a local web server:**
   
   **Option A - Python HTTP Server (Recommended):**
   ```bash
   python -m http.server 8000
   ```
   
   **Option B - Node.js http-server:**
   ```bash
   npx http-server -p 8000
   ```
   
   **Option C - VS Code Live Server:**
   - Install "Live Server" extension
   - Right-click on `index.html` → "Open with Live Server"

3. **Open your browser:**
   ```
   http://localhost:8000
   ```

### Step 2: Verify Website Functionality

✅ **Navigation Test:**
- Click on each tab: About, Projects, Interiors, Contact
- Verify smooth scrolling between sections
- Check URL hash changes (e.g., `#about`, `#projects`)

✅ **Responsive Design Test:**
- Open browser DevTools (F12)
- Toggle device toolbar (Ctrl+Shift+M)
- Test on different screen sizes:
  - Mobile (375px, 414px)
  - Tablet (768px, 1024px)
  - Desktop (1280px, 1920px)

✅ **Content Verification:**
- **About Section:**
  - Verify all text content displays correctly
  - Check services list renders properly
  
- **Projects Section:**
  - Verify all 6 project cards display
  - Check hover effects work
  - Verify project types show correctly

- **Interiors Section:**
  - Check gallery items display
  - Verify design process list shows
  
- **Contact Section:**
  - Test contact form validation:
    - Try submitting empty form (should show error)
    - Enter invalid email (should show error)
    - Submit valid form (should show success message)

✅ **Browser Console Check:**
- Open DevTools Console (F12)
- Look for any JavaScript errors
- Verify no 404 errors for assets

✅ **Cross-Browser Testing:**
- Test in multiple browsers:
  - Chrome
  - Firefox
  - Edge
  - Safari (if on Mac)

## 🔍 Common Issues & Solutions

### Issue: Blank Page or 404 Error
**Solution:**
- Ensure you're running the server from the `frontend` directory
- Check that `index.html` exists in the frontend directory
- Verify the server is running on port 8000

### Issue: CSS Not Loading
**Solution:**
- Check browser console for 404 errors
- Verify `css/style.css` exists in `frontend/css/` directory
- Check file paths are correct (relative paths)

### Issue: JavaScript Not Working
**Solution:**
- Check browser console for errors
- Verify `js/app.js` exists in `frontend/js/` directory
- Check that script tag in HTML is correct: `<script src="js/app.js"></script>`

### Issue: Navigation Not Working
**Solution:**
- Check browser console for JavaScript errors
- Verify `app.js` is loaded (check Network tab in DevTools)
- Test with JavaScript enabled in browser

### Issue: Mobile Menu Not Working
**Solution:**
- Resize browser window to mobile size (< 768px)
- Click hamburger menu icon
- Verify menu opens/closes

## 📝 Testing Checklist

Use this checklist to ensure everything works:

- [ ] Website loads on `http://localhost:8000`
- [ ] All navigation tabs work (About, Projects, Interiors, Contact)
- [ ] URL hash changes when clicking tabs
- [ ] No console errors
- [ ] All sections display correctly
- [ ] Responsive design works (mobile, tablet, desktop)
- [ ] Images/placeholders display (if any)
- [ ] Contact form validation works
- [ ] Form shows success message on valid submission
- [ ] Smooth scrolling works
- [ ] Hover effects work on project cards
- [ ] Mobile hamburger menu works
- [ ] Hero button links to About section

## 🎯 Next Steps

Once local testing passes:

1. **Review all functionality** - Make sure everything works as expected
2. **Optimize assets** - Compress images, minify CSS/JS if needed
3. **Test in different browsers** - Ensure cross-browser compatibility
4. **Check accessibility** - Test keyboard navigation, screen reader compatibility

After successful local testing, proceed to AWS deployment using:
```bash
cdk deploy
```

Or use the deployment scripts:
- Windows: `.\scripts\deploy.ps1`
- Linux/Mac: `./scripts/deploy.sh`
- Python: `python scripts/deploy.py`

## 💡 Tips

- Keep the local server running while making changes
- Use browser DevTools to debug issues
- Test frequently during development
- Use browser's "Hard Refresh" (Ctrl+Shift+R) to clear cache

