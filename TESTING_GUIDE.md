# 🧪 Complete Testing Guide - Verify All Features

## Quick Test Checklist

Use this guide to systematically test every feature of your Ecoreborn website.

---

## ✅ TEST 1: Home Page

**URL:** http://127.0.0.1:5000/

### What to Verify:
- [ ] Hero section displays "Reborn fabrics. Reborn future."
- [ ] Mission statement is visible
- [ ] 4 benefit cards display (Recycled, Eco-Friendly, Quality, B2B)
- [ ] 4-step process with icons is visible
- [ ] "Explore Services" button works
- [ ] "Contact Us" button works
- [ ] Newsletter form in footer
- [ ] Enter email and click Subscribe
- [ ] Should see success message "Thank you for subscribing!"
- [ ] Navigation menu works (all links clickable)
- [ ] Footer has social media links
- [ ] Page is responsive (resize browser window)

**Expected Result:** ✅ All elements visible, newsletter subscription works

---

## ✅ TEST 2: Services Page

**URL:** http://127.0.0.1:5000/services

### What to Verify:
- [ ] 5 services are listed:
  1. Fabric Recycling
  2. Custom Re-spun Fabric Orders
  3. B2B Partnerships
  4. Consulting for Textile Brands
  5. Student/Community Collection Drives
- [ ] Each service shows description and pricing
- [ ] Each service has a "Request This Service" form
- [ ] FAQ section at bottom
- [ ] Click on FAQ items to expand/collapse (no JavaScript!)

### Test Service Request Form:
1. **Fill in the form:**
   - Service: Select "Custom Re-spun Fabric Orders"
   - Name: Your Name
   - Email: test@example.com
   - Phone: 1234567890
   - Company: Test Company
   - Message: I need custom fabric for my fashion line

2. **Click "Submit Request"**

3. **Expected Result:**
   - [ ] Success message: "Your service request has been submitted successfully!"
   - [ ] Form clears
   - [ ] Check `logs/email.log` - should see confirmation email
   - [ ] Check `logs/email.log` - should see admin notification

### Test Form Validation:
1. **Try submitting with empty fields** → Should see error messages
2. **Try invalid email** → Should see "Invalid email address"
3. **Try very short message (< 10 chars)** → Should see error

**Expected Result:** ✅ All validations work, successful submission saves to database

---

## ✅ TEST 3: Contact Page

**URL:** http://127.0.0.1:5000/contact

### What to Verify:
- [ ] Contact form displays
- [ ] Contact information cards show:
  - Office address (Mumbai, India)
  - Email (contact@ecoreborn.example)
  - Phone (+91 98765 43210)
  - Business hours
- [ ] Map placeholder image displays

### Test Contact Form WITHOUT File:
1. **Fill in the form:**
   - Name: John Doe
   - Email: john@example.com
   - Subject: Question about services
   - Message: I would like to know more about your recycling process.

2. **Click "Send Message"**

3. **Expected Result:**
   - [ ] Success message: "Thank you for your message!"
   - [ ] Form clears
   - [ ] Check `logs/email.log` for confirmation email
   - [ ] Check `logs/email.log` for admin notification

### Test Contact Form WITH File:
1. **Prepare a test file:**
   - Create a small text file (test.txt) or use any PDF/image
   - File must be under 2MB

2. **Fill in the form:**
   - Name: Jane Smith
   - Email: jane@example.com
   - Subject: Project proposal
   - Message: Please see the attached proposal document.
   - Attachment: Select your test file

3. **Click "Send Message"**

4. **Expected Result:**
   - [ ] Success message appears
   - [ ] Check `uploads/` folder - file should be saved with timestamp
   - [ ] Check `logs/email.log` - should mention filename

### Test File Upload Validation:
1. **Try uploading large file (>2MB)** → Should see error
2. **Try invalid file type** (e.g., .exe) → Should see error

**Expected Result:** ✅ Form works with/without files, validation works

---

## ✅ TEST 4: Signup (Create New Account)

**URL:** http://127.0.0.1:5000/signup

### Test Successful Signup:
1. **Fill in the form:**
   - Full Name: Test User
   - Email: testuser@example.com
   - Password: MyPassword123
   - Confirm Password: MyPassword123

2. **Click "Sign Up"**

3. **Expected Result:**
   - [ ] Success message: "Account created successfully!"
   - [ ] Redirects to login page
   - [ ] User saved in database

### Test Signup Validation:
1. **Try weak password** (e.g., "123") → Should see error
2. **Try password mismatch** → Should see "Passwords must match"
3. **Try duplicate email** → Should see "Email already registered"
4. **Try invalid email** → Should see validation error

**Expected Result:** ✅ Validation works, successful signup creates account

---

## ✅ TEST 5: Login

**URL:** http://127.0.0.1:5000/login

### Test Admin Login:
1. **Fill in the form:**
   - Email: admin@ecoreborn.example
   - Password: Ec0r3b0rn!
   - Check "Remember me"

2. **Click "Log In"**

3. **Expected Result:**
   - [ ] Success message: "Welcome back!"
   - [ ] Redirects to dashboard
   - [ ] Navigation shows "Dashboard" link
   - [ ] Navigation shows "Logout" link

### Test Login with Your New Account:
1. **Use the account created in TEST 4**
   - Email: testuser@example.com
   - Password: MyPassword123

2. **Click "Log In"**

3. **Expected Result:**
   - [ ] Successfully logs in
   - [ ] Redirects to dashboard

### Test Login Validation:
1. **Try wrong password** → Should see "Invalid email or password"
2. **Try nonexistent email** → Should see "Invalid email or password"
3. **Try 6 times with wrong password** → Should be rate limited

**Expected Result:** ✅ Login works, validation works, rate limiting works

---

## ✅ TEST 6: Dashboard (Logged In)

**URL:** http://127.0.0.1:5000/dashboard

**⚠️ You must be logged in to access this page**

### What to Verify:
- [ ] User information card displays:
  - Your name
  - Your email
  - Account created date
- [ ] "Your Service Requests" section shows
- [ ] If you submitted service requests in TEST 2, they appear in table
- [ ] Each request shows:
  - Date
  - Service name
  - Status badge (Pending/In Progress/Completed)
  - Message preview
- [ ] Quick actions links work
- [ ] "Request New Service" link goes to services page
- [ ] "Contact Support" link goes to contact page
- [ ] Logout button visible

**Expected Result:** ✅ Dashboard shows user data and service requests

---

## ✅ TEST 7: Forgot Password

**URL:** http://127.0.0.1:5000/forgot-password

### Test Password Reset Request:
1. **Fill in the form:**
   - Email: testuser@example.com (or admin@ecoreborn.example)

2. **Click "Request Password Reset"**

3. **Expected Result:**
   - [ ] Success message: "If the email exists, a reset link has been sent"
   - [ ] Check `logs/email.log` for reset email
   - [ ] Email contains reset link like: `http://localhost:5000/reset-password/abc123token`

4. **Copy the token from the email log**

**Expected Result:** ✅ Reset request works, token generated and emailed

---

## ✅ TEST 8: Reset Password (Use Token)

**URL:** http://127.0.0.1:5000/reset-password/{token}

**Replace {token} with the token from TEST 7**

### Test Password Reset:
1. **Paste full URL with token in browser**

2. **Fill in the form:**
   - New Password: NewPassword456
   - Confirm Password: NewPassword456

3. **Click "Reset Password"**

4. **Expected Result:**
   - [ ] Success message: "Password has been reset successfully"
   - [ ] Redirects to login page
   - [ ] Can now login with new password

5. **Try logging in with NEW password:**
   - Email: testuser@example.com
   - Password: NewPassword456

6. **Should successfully log in**

### Test Token Validation:
1. **Try using expired/invalid token** → Should see error
2. **Try using same token twice** → Should see error

**Expected Result:** ✅ Password reset works, old password invalid, new password works

---

## ✅ TEST 9: Logout

**Click "Logout" from navigation or dashboard**

### Expected Result:
- [ ] Success message: "You have been logged out"
- [ ] Redirects to home page
- [ ] Navigation no longer shows "Dashboard" or "Logout"
- [ ] Trying to access http://127.0.0.1:5000/dashboard redirects to login

**Expected Result:** ✅ Logout works, session cleared

---

## ✅ TEST 10: Protected Route Security

### Test Without Login:
1. **Logout if currently logged in**

2. **Try accessing dashboard directly:**
   - URL: http://127.0.0.1:5000/dashboard

3. **Expected Result:**
   - [ ] Redirects to login page
   - [ ] Shows message: "Please log in to access this page"

4. **After logging in:**
   - [ ] Automatically redirects back to dashboard

**Expected Result:** ✅ Protected routes require authentication

---

## ✅ TEST 11: Error Pages

### Test 404 Page:
1. **Visit non-existent URL:**
   - http://127.0.0.1:5000/nonexistent-page

2. **Expected Result:**
   - [ ] Shows custom 404 page
   - [ ] Page says "Page Not Found"
   - [ ] Has navigation links back to main site

### Test File Upload Size Limit (413 Error):
1. **Try uploading file larger than 2MB on contact page**

2. **Expected Result:**
   - [ ] Shows error message about file size

**Expected Result:** ✅ Error pages work correctly

---

## ✅ TEST 12: SEO & Meta Pages

### Test Sitemap:
**URL:** http://127.0.0.1:5000/sitemap.xml

**Expected Result:**
- [ ] Shows XML format
- [ ] Lists all public pages
- [ ] Includes priority and frequency

### Test Robots.txt:
**URL:** http://127.0.0.1:5000/robots.txt

**Expected Result:**
- [ ] Shows text format
- [ ] Allows all user agents
- [ ] Disallows /dashboard
- [ ] Links to sitemap

**Expected Result:** ✅ SEO files work

---

## ✅ TEST 13: Responsive Design

### Test Mobile View:
1. **Resize browser to phone width (375px)**

2. **Verify:**
   - [ ] Navigation collapses or wraps
   - [ ] Content stacks vertically
   - [ ] Forms are usable
   - [ ] Buttons are tappable
   - [ ] Text is readable (no horizontal scroll)

### Test Tablet View:
1. **Resize browser to tablet width (768px)**

2. **Verify:**
   - [ ] Layout adjusts appropriately
   - [ ] All content visible

### Test Desktop View:
1. **Maximize browser window (1920px+)**

2. **Verify:**
   - [ ] Content uses full width efficiently
   - [ ] No elements cut off

**Expected Result:** ✅ Website works on all screen sizes

---

## ✅ TEST 14: Accessibility

### Test Keyboard Navigation:
1. **Use only TAB key to navigate**

2. **Verify:**
   - [ ] Can reach all links and buttons
   - [ ] Can see focus indicators
   - [ ] Can submit forms with Enter key
   - [ ] Can use arrow keys in dropdowns

### Test Screen Reader (Optional):
1. **Enable screen reader** (Windows: Narrator, Mac: VoiceOver)

2. **Verify:**
   - [ ] All images have alt text
   - [ ] Form labels are announced
   - [ ] Page structure is logical

**Expected Result:** ✅ Website is accessible

---

## ✅ TEST 15: No JavaScript Verification

### Verify Zero JavaScript:
1. **Open browser DevTools** (F12)

2. **Go to Console tab**

3. **Visit all pages**

4. **Expected Result:**
   - [ ] No JavaScript errors (because there's no JavaScript!)
   - [ ] No external JS files loaded
   - [ ] All features work without JS

5. **Disable JavaScript in browser:**
   - Chrome: Settings → Privacy → Site Settings → JavaScript → Block
   - Firefox: about:config → javascript.enabled → false

6. **Test all features again**

7. **Expected Result:**
   - [ ] Everything still works exactly the same!

**Expected Result:** ✅ Confirmed zero JavaScript

---

## ✅ TEST 16: Database Verification

### Check MongoDB Collections:
1. **Login to MongoDB Atlas Dashboard**

2. **Navigate to your cluster**

3. **Browse Collections**

4. **Verify collections exist:**
   - [ ] users
   - [ ] password_reset_tokens
   - [ ] contact_messages
   - [ ] service_requests
   - [ ] newsletter_subscribers
   - [ ] login_attempts

5. **Check data:**
   - [ ] Admin user exists
   - [ ] Your test data is saved
   - [ ] Timestamps are correct

**Expected Result:** ✅ All data saved correctly

---

## ✅ TEST 17: Email Logging

### Check Email Logs:
1. **Open file:** `c:\Users\siddh\Desktop\EcoReborn\logs\email.log`

2. **Verify emails logged:**
   - [ ] Password reset emails
   - [ ] Contact form confirmations
   - [ ] Service request confirmations
   - [ ] Admin notifications
   - [ ] Newsletter confirmations

3. **Each email should have:**
   - [ ] Timestamp
   - [ ] Recipient
   - [ ] Subject
   - [ ] Full body content

**Expected Result:** ✅ All emails logged properly

---

## ✅ TEST 18: File Uploads

### Check Upload Directory:
1. **Open folder:** `c:\Users\siddh\Desktop\EcoReborn\uploads\`

2. **Verify:**
   - [ ] Uploaded files are saved
   - [ ] Filenames are sanitized (timestamp prefix)
   - [ ] Files are complete and not corrupted

3. **Try opening uploaded files** → Should work

**Expected Result:** ✅ Files saved securely

---

## ✅ TEST 19: Security Features

### Test CSRF Protection:
1. **Open browser DevTools**

2. **Inspect any form**

3. **Verify:**
   - [ ] Hidden input field with name "csrf_token"
   - [ ] Token is unique per session

### Test Rate Limiting:
1. **Try logging in with wrong password 6 times**

2. **Expected Result:**
   - [ ] After 5 attempts, should be blocked
   - [ ] Error message: "Too many login attempts"
   - [ ] Wait 15 minutes or restart server to reset

### Test Password Security:
1. **Check database** (MongoDB Atlas)

2. **Look at users collection**

3. **Verify:**
   - [ ] Passwords are hashed (not plaintext)
   - [ ] Hashes start with `$2b$` (bcrypt)

**Expected Result:** ✅ All security features working

---

## ✅ TEST 20: Performance

### Test Page Load Speed:
1. **Open browser DevTools → Network tab**

2. **Visit each page and measure load time:**
   - [ ] Home page: < 500ms
   - [ ] Services page: < 500ms
   - [ ] Contact page: < 500ms
   - [ ] Dashboard: < 500ms

3. **Check number of requests:**
   - [ ] Minimal HTTP requests (no external JS/CSS)
   - [ ] Only HTML, CSS, images

**Expected Result:** ✅ Fast page loads

---

## 🎯 Final Verification

### Complete Feature Checklist:

**Authentication:**
- [x] Signup works
- [x] Login works
- [x] Logout works
- [x] Password reset works
- [x] Session management works
- [x] Protected routes work

**Forms:**
- [x] Contact form works
- [x] Service request form works
- [x] Newsletter form works
- [x] All validation works
- [x] File upload works

**Pages:**
- [x] Home page renders
- [x] Services page renders
- [x] Contact page renders
- [x] Dashboard renders
- [x] Error pages render

**Security:**
- [x] CSRF protection enabled
- [x] Rate limiting works
- [x] Password hashing works
- [x] File upload security works

**Database:**
- [x] MongoDB connected
- [x] Data saves correctly
- [x] Queries work

**Email:**
- [x] Email logging works
- [x] All email types send

**Design:**
- [x] Responsive design works
- [x] No JavaScript used
- [x] Accessibility features work

---

## 🐛 If Something Doesn't Work

### Troubleshooting Steps:

1. **Check server is running:**
   - Terminal should show: "Running on http://127.0.0.1:5000"
   - If not, run: `python app.py`

2. **Check MongoDB connection:**
   - Verify `.env` has correct MONGODB_URI
   - Check MongoDB Atlas is accessible

3. **Check logs:**
   - Terminal output shows errors
   - `logs/email.log` for email issues

4. **Check file permissions:**
   - `uploads/` folder must be writable
   - `logs/` folder must be writable

5. **Clear browser cache:**
   - Hard refresh: Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)

6. **Restart server:**
   - Stop: Ctrl+C
   - Start: `python app.py`

---

## ✅ Test Results Summary

After completing all tests, fill in:

- **Total Tests:** 20
- **Tests Passed:** _____
- **Tests Failed:** _____
- **Issues Found:** _____

### Your Notes:
```
[Write any issues or observations here]
```

---

## 🎉 All Tests Passed?

**Congratulations!** Your Ecoreborn website is fully functional and production-ready!

### Next Steps:
1. Customize content and styling
2. Replace placeholder images
3. Configure real SMTP for email
4. Deploy to production (see DEPLOYMENT.md)
5. Set up custom domain
6. Enable SSL certificate

---

**Testing completed on:** _______________
**Tested by:** _______________
**Status:** ⬜ PASS  ⬜ FAIL  ⬜ NEEDS WORK
