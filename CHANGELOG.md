# Changelog

All notable changes to the Ecoreborn website project will be documented in this file.

## [1.0.0] - 2025-11-11

### Added
- Initial release of Ecoreborn sustainable fashion website
- User authentication system (signup, login, logout)
- Password reset functionality with email simulation
- Home page with hero section, benefits, and circular process explanation
- Services page with 5 core services and request forms
- Contact page with file upload support
- User dashboard for managing service requests
- Newsletter subscription system
- Server-side form validation and CSRF protection
- Rate limiting on authentication routes
- MongoDB Atlas integration for data persistence
- Email simulation via file logging (logs/email.log)
- Fully responsive CSS-only design (no JavaScript)
- SEO optimization (meta tags, sitemap.xml, robots.txt)
- Accessibility features (semantic HTML, ARIA labels, keyboard navigation)
- Print stylesheet for document printing
- Error pages (404, 500)
- Comprehensive documentation (README, DEPLOYMENT, MAINTAINERS)

### Security
- Bcrypt password hashing
- Secure session cookies
- Input validation and sanitization
- File upload restrictions (2MB, safe extensions)
- CSRF protection on all forms
- SQL injection prevention via ORM
- XSS prevention via template auto-escaping
- Rate limiting on login attempts

### Technical
- Python 3.11+ with Flask framework
- MongoDB Atlas cloud database
- Jinja2 template engine
- Flask-Login for authentication
- Flask-WTF for forms and CSRF
- Flask-Limiter for rate limiting
- Pytest for testing
- Mobile-first responsive design
- CSS Grid and Flexbox layouts
- Web fonts (Google Fonts with fallbacks)
- SVG icons for scalability

## [Future Releases]

### Planned Features
- Admin panel for managing service requests and contact messages
- Email notifications via SMTP
- Advanced search and filtering
- User profile editing
- Service request status tracking
- Export functionality for requests
- Multi-language support
- Dark mode toggle
- Progressive Web App (PWA) capabilities
