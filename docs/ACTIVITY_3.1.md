Activity 3.1: User Interface and Multi-Tab Layout Design

Overview

This activity documents the structured multi-tab user interface design implemented throughout Activities 1.3, 2.1, 2.2, and 2.3. The MedSafe AI platform features a professional, responsive layout with clear visual hierarchy, consistent styling, and intuitive navigation across all core functionalities.

Objectives

1. Design structured multi-tab interface for core functionalities
2. Apply consistent styling and layout using Streamlit components
3. Ensure responsiveness across different screen sizes
4. Maintain professional appearance and readability
5. Implement clear visual hierarchy



UI Architecture

Application Structure

MedSafe AI - Intelligent Medicine Safety Assistant
├── Page Configuration (Wide layout, expanded sidebar)
├── Main Title and Branding
├── Sidebar Navigation (Radio buttons)
│   ├── 🏠 Home
│   ├── 💊 Medicine Interaction Checker
│   ├── 📄 Prescription OCR
│   ├── 🩺 Symptom & Doubt Solver
│   ├── ⚠️ Side-Effect Monitor
│   └── 🚨 Emergency Risk Predictor
└── Content Area (Dynamic based on selection)

Page Configuration

Settings:
- Page Title: "MedSafe AI"
- Page Icon: 💊
- Layout: Wide (maximizes screen space)
- Sidebar State: Expanded (always visible)

Code:
st.set_page_config(
    page_title="MedSafe AI",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

Main Header

Design:
- Large title with emoji icon
- Descriptive subtitle
- Horizontal separator for visual clarity

Implementation:
st.title("💊 MedSafe AI - AI-Driven Medical Safety Assistant")
st.markdown("---")

Sidebar Navigation

Design Principles:
- Fixed left sidebar
- Radio button selection (single choice)
- Icon-based navigation
- Clear module names
- Persistent across sessions

Navigation Items:
1. 🏠 Home - Welcome and overview
2. 💊 Medicine Interaction Checker - Drug interaction analysis
3. 📄 Prescription OCR - Image-based medicine extraction
4. 🩺 Symptom & Doubt Solver - Symptom guidance
5. ⚠️ Side-Effect Monitor - Post-medication analysis
6. 🚨 Emergency Risk Predictor - Risk assessment

Implementation:
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Module:",
    [list of pages with icons]
)

Tab Designs

1. Home Tab (🏠)

Purpose: Welcome page and feature overview

Layout:
- Welcome header
- Platform description
- Key features list
- Educational disclaimer

Content Sections:
- Introduction paragraph
- Feature highlights (bullet points)
- Disclaimer note

Visual Elements:
- Clean typography
- Bullet point lists
- Informative text

Implementation Status: ✅ Complete

2. Medicine Interaction Checker Tab (💊)

Purpose: Check drug-drug interactions with fuzzy matching

Layout:
- Header with description
- Input section (text area)
- Action buttons (Check Interactions, Clear)
- Results display (multi-section)

Input Components:
- Multi-line text area (150px height)
- Placeholder text with examples
- Primary action button
- Secondary clear button

Results Display:
Section 1: Medicine Identification
- Color-coded status (green/blue/red)
- Confidence scores
- Exact vs fuzzy matches

Section 2: Interaction Analysis
- Severity-based warnings (high/moderate/low)
- Medicine pairs
- Detailed descriptions

Section 3: Individual Warnings
- Expandable sections per medicine
- Grapefruit warnings
- Known interactions

Footer:
- Educational disclaimer

Visual Hierarchy:
- Clear section headers (###)
- Color coding by severity
- Expandable details
- Prominent disclaimers

Implementation Status: ✅ Complete (Activity 2.1)

3. Prescription OCR Tab (📄)

Purpose: Extract medicines from prescription images using AI

Layout:
- Header with description
- File uploader
- Image preview (2-column layout)
- Extraction options
- Multi-step results display

Input Components:
- File uploader (JPG, JPEG, PNG)
- Image preview with metadata
- Extract button (primary)
- AI parsing checkbox

Results Display:
Step 1: OCR Text Extraction
- Success indicator
- Raw text (expandable)

Step 2: Medicine Identification
- Extraction method indicator
- Detected medicines count
- Expandable medicine details

Step 3: Database Validation
- Fuzzy matching results
- Confidence scores
- Color-coded validation

Step 4: Interaction Analysis
- Automatic interaction checking
- Severity warnings
- Detailed descriptions

Step 5: Safety Recommendations
- Individual medicine warnings
- Expandable sections
- Educational disclaimer

Visual Hierarchy:
- Step-by-step progression
- Clear section markers
- Expandable details
- Loading spinners
- Color-coded results

Implementation Status: ✅ Complete (Activity 2.2)

4. Symptom & Doubt Solver Tab (🩺)

Purpose: Provide AI-enhanced symptom guidance

Layout:
- Header with description
- Symptom input (text area)
- Action buttons
- Multi-section results

Input Components:
- Large text area (150px height)
- Placeholder with example
- Get Guidance button (primary)
- AI analysis checkbox

Results Display:
- Severity indicator (color-coded)
- Detected symptoms list
- AI educational explanation
- Home remedies section
- Lifestyle suggestions section
- Warning signs (red alerts)
- Educational disclaimer

Visual Hierarchy:
- Severity at top (prominent)
- Sectioned content
- Bullet point lists
- Red warning signs
- Clear disclaimers

Implementation Status: ✅ Complete (Activity 2.3)

5. Side-Effect Monitor Tab (⚠️)

Purpose: Analyze post-medication experiences

Layout:
- Header with description
- Input form (2-column)
- Experience text area
- Action buttons
- Results display

Input Components:
Column 1:
- Age (number input)
- Gender (select box)

Column 2:
- Medicine name (text input)
- Dosage (text input)

Full Width:
- Experience description (text area)
- Analyze button (primary)
- AI analysis checkbox

Results Display:
- Severity indicator (severe/moderate/mild)
- Medicine information summary
- AI analysis section
- Severity-based recommendation
- Educational disclaimer

Visual Hierarchy:
- Severity prominent
- Organized information
- Clear recommendations
- Color-coded severity

Implementation Status: ✅ Complete (Activity 2.3)

6. Emergency Risk Predictor Tab (🚨)

Purpose: Calculate emergency risk scores

Layout:
- Header with description
- Input form (2-column)
- Symptom text area
- Severity slider
- Action buttons
- Comprehensive results display

Input Components:
Column 1:
- Age (optional, number input)
- Gender (optional, select box)

Column 2:
- Medical history (multi-select)

Full Width:
- Symptoms description (text area)
- Severity slider (1-10)
- Calculate Risk button (primary)
- AI safety note checkbox

Results Display:
- Large risk score percentage
- Color-coded risk level (HIGH/MEDIUM/LOW)
- Risk factors list
- Affected body systems
- AI safety guidance
- Clear recommendation
- Expandable calculation details
- Prominent emergency disclaimer

Visual Hierarchy:
- Risk score center-prominent
- Color-coded levels
- Sectioned information
- Expandable details
- Critical disclaimers

Implementation Status: ✅ Complete (Activity 2.3)

Design Principles

1. Consistency

Typography:
- Headers: Streamlit default (consistent sizing)
- Body text: Readable font size
- Code blocks: Monospace for technical content

Spacing:
- Consistent padding between sections
- Horizontal separators (---) between major sections
- Proper whitespace for readability

Color Coding:
- Green (✅): Success, exact matches, low risk
- Blue (ℹ️): Information, fuzzy matches, medium risk
- Yellow (⚠️): Warnings, moderate severity
- Red (🚨): Errors, high severity, emergencies

Icons:
- Consistent emoji usage
- Meaningful visual indicators
- Enhanced readability

2. Responsiveness

Layout Strategies:
- Wide layout for desktop optimization
- Column layouts (st.columns) for side-by-side content
- Expandable sections (st.expander) for details
- Responsive text areas and inputs

Screen Size Handling:
- Streamlit's built-in responsiveness
- Flexible column widths
- Collapsible sidebar
- Scrollable content areas

Device Compatibility:
- Desktop: Full wide layout
- Tablet: Responsive columns
- Mobile: Stacked layout (Streamlit default)

3. Visual Hierarchy

Information Architecture:
- Primary actions: Prominent buttons (type="primary")
- Secondary actions: Standard buttons
- Tertiary information: Expandable sections

Content Organization:
- Headers (###) for major sections
- Subheaders for subsections
- Bullet points for lists
- Horizontal separators for divisions

Emphasis Techniques:
- Bold text for important terms
- Color coding for severity
- Icons for visual scanning
- Expandable details for optional content

4. User Experience

Interaction Patterns:
- Clear call-to-action buttons
- Immediate feedback (spinners, messages)
- Progressive disclosure (expandable sections)
- Persistent navigation (sidebar)

Feedback Mechanisms:
- Success messages (st.success)
- Warning messages (st.warning)
- Error messages (st.error)
- Info messages (st.info)
- Loading spinners (st.spinner)

Guidance:
- Placeholder text in inputs
- Help text on hover
- Instructions when no input
- Examples provided
- Clear disclaimers

5. Accessibility

Readability:
- Clear font sizes
- Sufficient contrast
- Proper spacing
- Logical reading order

Navigation:
- Keyboard accessible (Streamlit default)
- Clear focus indicators
- Logical tab order
- Consistent navigation

Content:
- Descriptive labels
- Clear instructions
- Alternative text for icons (emoji)
- Structured headings

Component Library

Streamlit Components Used:

Input Components:
- st.text_area(): Multi-line text input
- st.text_input(): Single-line text input
- st.number_input(): Numeric input
- st.selectbox(): Dropdown selection
- st.multiselect(): Multiple selection
- st.slider(): Range selection
- st.checkbox(): Boolean toggle
- st.button(): Action trigger
- st.file_uploader(): File upload
- st.radio(): Single choice selection

Display Components:
- st.title(): Main page title
- st.header(): Section headers
- st.subheader(): Subsection headers
- st.markdown(): Formatted text
- st.write(): General text output
- st.success(): Success messages
- st.warning(): Warning messages
- st.error(): Error messages
- st.info(): Information messages
- st.image(): Image display
- st.expander(): Collapsible sections

Layout Components:
- st.columns(): Multi-column layout
- st.sidebar: Sidebar container
- st.spinner(): Loading indicator
- st.markdown("---"): Horizontal separator

Session State:
- st.session_state: Persistent data storage
- Caching for performance
- State management across interactions

Color Scheme

Primary Colors:
- Success Green: Streamlit default green
- Warning Yellow: Streamlit default yellow
- Error Red: Streamlit default red
- Info Blue: Streamlit default blue

Background:
- Light mode: White/light gray
- Dark mode: Dark gray/black (Streamlit theme)

Text:
- Primary: Black/white (theme dependent)
- Secondary: Gray
- Links: Blue

Accents:
- Icons: Emoji colors
- Buttons: Streamlit primary blue
- Highlights: Theme-based

Typography

Font Family:
- Streamlit default (system fonts)
- Sans-serif for readability
- Monospace for code

Font Sizes:
- Title: Large (st.title)
- Headers: Medium-large (st.header)
- Subheaders: Medium (st.subheader)
- Body: Standard (st.write)
- Small: Reduced (markdown)

Font Weights:
- Bold: Important terms
- Regular: Body text
- Light: Secondary information

Line Height:
- Comfortable reading spacing
- Streamlit default optimization

Spacing System

Vertical Spacing:
- Between sections: Horizontal separator (---)
- Between elements: Streamlit default
- Within sections: Natural flow

Horizontal Spacing:
- Columns: Equal or proportional (st.columns)
- Margins: Streamlit default
- Padding: Consistent throughout

Content Spacing:
- Text areas: 150px height (standard)
- Buttons: Grouped logically
- Forms: Organized in columns

Responsive Behavior

Desktop (>1024px):
- Wide layout active
- Sidebar expanded
- Multi-column layouts
- Full feature display

Tablet (768px-1024px):
- Responsive columns
- Sidebar collapsible
- Stacked when needed
- Touch-friendly targets

Mobile (<768px):
- Single column layout
- Collapsible sidebar
- Stacked elements
- Mobile-optimized inputs

Performance Optimization

Loading Strategies:
- Session state caching
- Lazy loading of modules
- Efficient re-rendering
- Minimal state updates

User Feedback:
- Loading spinners for long operations
- Immediate button feedback
- Progress indicators
- Clear status messages

Resource Management:
- Cached database loading
- Reused analyzer instances
- Efficient image handling
- Optimized AI calls

Testing and Validation

UI Testing Checklist:

Navigation:
- ✅ All tabs accessible
- ✅ Sidebar navigation works
- ✅ Page state persists
- ✅ No broken links

Layout:
- ✅ Responsive on desktop
- ✅ Readable typography
- ✅ Proper spacing
- ✅ Visual hierarchy clear

Functionality:
- ✅ All buttons work
- ✅ Inputs accept data
- ✅ Results display correctly
- ✅ Error handling works

Accessibility:
- ✅ Keyboard navigation
- ✅ Clear labels
- ✅ Sufficient contrast
- ✅ Logical structure

Performance:
- ✅ Fast page loads
- ✅ Smooth interactions
- ✅ No lag or freezing
- ✅ Efficient rendering

Browser Compatibility:

Tested Browsers:
- Chrome: ✅ Full support
- Firefox: ✅ Full support
- Safari: ✅ Full support
- Edge: ✅ Full support

Known Issues:
- None reported

Future Enhancements

Planned Improvements:

1. Enhanced Styling
   - Custom CSS themes
   - Brand colors
   - Custom fonts
   - Advanced animations

2. Additional Features
   - User accounts
   - History tracking
   - Export functionality
   - Print-friendly views

3. Advanced Interactions
   - Drag-and-drop
   - Real-time updates
   - Keyboard shortcuts
   - Advanced filtering

4. Mobile Optimization
   - Native mobile app
   - Progressive web app
   - Touch gestures
   - Mobile-specific UI

Deliverables

1. Multi-Tab Interface
   - 6 functional tabs
   - Consistent navigation
   - Clear organization

2. Responsive Layout
   - Wide layout design
   - Column-based organization
   - Expandable sections

3. Professional Styling
   - Consistent typography
   - Color-coded feedback
   - Clear visual hierarchy

4. User Experience
   - Intuitive navigation
   - Clear instructions
   - Immediate feedback
   - Educational disclaimers

5. Documentation
   - This activity documentation
   - Design principles
   - Component library
   - Testing results


