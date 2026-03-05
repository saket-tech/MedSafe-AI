Activity 3.3: Output Rendering and Data Visualization

Overview

This activity documents the comprehensive output rendering and data visualization implementation across all MedSafe AI modules. The system displays extracted medicines, interaction warnings, symptom guidance, and AI-generated explanations in a structured, readable format using color-coded alerts, metrics, expandable sections, and clear visual indicators to support rapid understanding and safe decision-making.

Objectives

1. Display extracted data in structured, readable format
2. Render emergency risk scores with visual indicators
3. Present raw OCR text and structured JSON outputs
4. Provide real-time color-coded feedback messages
5. Ensure transparency and traceability of AI-assisted results


Output Rendering Strategies

1. Color-Coded Message System

Purpose: Provide immediate visual feedback on result severity and status

Message Types:

A. Success Messages (st.success - Green)

Usage:
- Exact medicine matches found
- No interactions detected
- Text extraction successful
- Analysis completed successfully

Implementation Examples:
st.success("✅ Text extracted successfully!")
st.success(f"✅ {med_input} → Exact match: {match['data']['name']}")
st.success("✅ No known interactions detected between these medicines")
st.success(f"✅ Found {len(medicines)} medicine(s)")

Visual Characteristics:
- Green background
- Checkmark emoji (✅)
- Positive reinforcement
- Clear success indicator

B. Information Messages (st.info - Blue)

Usage:
- Fuzzy match results
- Extraction method indicators
- Educational explanations
- General guidance
- Disclaimers

Implementation Examples:
st.info(f"🔍 {med_input} → Found: {match['data']['name']} (Confidence: {confidence}%)")
st.info(f"Extraction Method: {structured_data.get('extraction_method', 'Unknown')}")
st.info(analysis['ai_explanation'])
st.info("📌 Disclaimer: This is an educational tool...")

Visual Characteristics:
- Blue background
- Information emoji (ℹ️)
- Neutral tone
- Informative content

C. Warning Messages (st.warning - Yellow)

Usage:
- Moderate severity interactions
- Partial results
- Validation warnings
- Caution advisories

Implementation Examples:
st.warning(f"Found {len(interactions)} potential interaction(s)")
st.warning(f"Interaction {idx}: MODERATE SEVERITY")
st.warning(f"⚠️ {med_name} → Not found in database")
st.warning("⚠️ Severity: MODERATE")

Visual Characteristics:
- Yellow/orange background
- Warning emoji (⚠️)
- Cautionary tone
- Attention-grabbing

D. Error Messages (st.error - Red)

Usage:
- High severity interactions
- Critical warnings
- Extraction failures
- Emergency indicators

Implementation Examples:
st.error(f"Interaction {idx}: HIGH SEVERITY")
st.error(f"🚨 Severity Level: HIGH")
st.error(f"🚨 {warning}")
st.error("❌ No text could be extracted from the image")

Visual Characteristics:
- Red background
- Error/alert emoji (🚨, ❌)
- Urgent tone
- Critical information

2. Structured Data Display

A. Medicine Interaction Checker Output

Section 1: Medicine Identification
Format:
✅ Atorvastatin → Exact match: Atorvastatin (100%)
🔍 Ibuprofin → Found: Ibuprofen (89%)
❌ UnknownMed → Not found in database

Features:
- Color-coded by match quality
- Confidence scores displayed
- Clear match status
- Original vs corrected names

Section 2: Interaction Analysis
Format:
⚠️ Found 2 potential interaction(s)

Interaction 1: HIGH SEVERITY
Medicines: Ibuprofen + Warfarin
Description: Increased bleeding risk when combined

Features:
- Severity-based color coding
- Numbered interactions
- Medicine pairs clearly shown
- Detailed descriptions
- Visual separators

Section 3: Individual Medicine Warnings
Format:
▼ ⚠️ Atorvastatin - 2 warning(s)
  🍊 Grapefruit Warning: High - Avoid grapefruit juice
  💊 Known Interactions: clarithromycin, itraconazole

Features:
- Expandable sections (st.expander)
- Warning count in header
- Icon-based categorization
- Detailed warning information

B. Prescription OCR Output

Step 1: OCR Text Extraction
Format:
✅ Text extracted successfully!

▼ 📄 View Raw Extracted Text
  [Raw OCR text displayed in monospace]

Features:
- Success indicator
- Expandable raw text view
- Monospace formatting
- Transparency of extraction

Step 2: Medicine Identification
Format:
✅ Found 5 medicine(s)
ℹ️ Extraction Method: AI (LLaMA 3)

▼ Medicine 1: Atorvastatin
  Name: Atorvastatin        Active Salt: Atorvastatin
  Form: Tablet               Dosage: 10mg

Features:
- Medicine count
- Extraction method transparency
- Expandable medicine details
- Two-column layout
- Structured information

Step 3: Database Validation
Format:
✅ Atorvastatin → Found in database: Atorvastatin (100% match)
🔍 Ibuprofin → Possible match: Ibuprofen (85% match)
⚠️ CustomMed → Not found in database (may need manual verification)

Features:
- Fuzzy matching results
- Confidence scores
- Color-coded validation
- Manual verification prompts

Step 4: Interaction Analysis
Format:
🚨 Found 2 potential interaction(s)!

Interaction 1: HIGH SEVERITY
Medicines: Ibuprofen + Warfarin
Description: Increased bleeding risk when combined

Features:
- Automatic interaction checking
- Severity-based alerts
- Clear medicine pairs
- Detailed descriptions

Step 5: Safety Recommendations
Format:
▼ ⚠️ Atorvastatin - 2 warning(s)
  🍊 Grapefruit Warning: High - Avoid grapefruit juice
  💊 Known Interactions: clarithromycin, itraconazole

Features:
- Per-medicine warnings
- Expandable sections
- Icon categorization
- Comprehensive safety info

C. Symptom & Doubt Solver Output

Severity Indicator:
Format:
🚨 Severity Level: HIGH
⚠️ Severity Level: MEDIUM
ℹ️ Severity Level: LOW

Features:
- Color-coded by severity
- Prominent placement
- Clear visual hierarchy
- Emoji indicators

Detected Symptoms:
Format:
🔍 Detected Symptoms
• Fever
• Headache
• Dizziness

Features:
- Bullet point list
- Clear section header
- Simple presentation

AI Educational Explanation:
Format:
🤖 AI Educational Explanation
ℹ️ [AI-generated explanation in 2-3 sentences]

Features:
- Blue info box
- AI indicator
- Educational tone
- Concise content

Home Remedies:
Format:
🏠 Home Remedies
✓ Drink plenty of fluids
✓ Take lukewarm bath
✓ Use cool compress
✓ Wear light clothing

Features:
- Checkmark bullets
- Actionable items
- Clear formatting
- Practical advice

Lifestyle Suggestions:
Format:
💪 Lifestyle Suggestions
✓ Get adequate rest
✓ Avoid strenuous activity
✓ Stay in cool environment

Features:
- Checkmark bullets
- Long-term guidance
- Preventive measures

Warning Signs:
Format:
⚠️ Warning Signs - Seek Immediate Care If:
🚨 Temperature >103°F (39.4°C)
🚨 Fever lasting >3 days
🚨 Severe headache with fever
🚨 Difficulty breathing

Features:
- Red error boxes
- Emergency emoji
- Critical symptoms
- Clear action required

D. Side-Effect Monitor Output

Severity Indicator:
Format:
🚨 Severity: SEVERE
⚠️ Severity: MODERATE
ℹ️ Severity: MILD

Features:
- Color-coded severity
- Prominent display
- Clear categorization

Medicine Information:
Format:
💊 Medicine Information
Medicine: Ibuprofen          Age: 35
Dosage: 400mg                Gender: Male

Features:
- Two-column layout
- Key information
- Clear labels
- Organized display

AI Analysis:
Format:
🤖 AI Analysis
ℹ️ [AI-generated analysis in 2-3 sentences]

Features:
- Blue info box
- AI indicator
- Educational content
- Supportive tone

Recommendation:
Format:
📋 Recommendation
🚨 STOP taking the medicine and seek immediate medical attention...
⚠️ Contact your healthcare provider soon...
ℹ️ Monitor the side effects...

Features:
- Severity-based color coding
- Clear action items
- Specific guidance
- Appropriate urgency

E. Emergency Risk Predictor Output

Risk Score Display:
Format:
        85.5%
    🚨 HIGH RISK

Features:
- Large percentage display
- Color-coded risk level
- Center-aligned
- Prominent placement
- Three-column layout for centering

Risk Factors:
Format:
⚠️ Identified Risk Factors
• chest pain
• difficulty breathing
• Age factor: 65 years

Features:
- Bullet point list
- Clear identification
- Contributing factors
- Transparent calculation

Affected Systems:
Format:
🏥 Affected Systems
• Cardiac
• Respiratory

Features:
- Body system categories
- Medical terminology
- Clear organization

AI Safety Guidance:
Format:
🤖 AI Safety Guidance
ℹ️ [AI-generated safety note in 2-3 sentences]

Features:
- Blue info box
- Compassionate tone
- Educational emphasis
- Supportive guidance

Recommendation:
Format:
📋 Recommendation
 SEEK IMMEDIATE MEDICAL ATTENTION. Call emergency services (911)...
⚠️ CONSULT A HEALTHCARE PROVIDER SOON. Schedule appointment within 24 hours...
ℹ️ MONITOR SYMPTOMS. Consider consulting if symptoms persist...

Features:
- Risk-level based color
- Clear action verbs
- Specific timeframes
- Emergency contact info

Calculation Details (Expandable):
Format:
▼ 🔍 View Calculation Details
  Base Score: 165.0
  Severity Factor: 0.8
  Age Factor: 1.2
  Medical History Factor: 1.15
  Final Score: 85.5%

Features:
- Expandable section
- Transparent calculation
- All factors shown
- Mathematical breakdown
- Builds trust

3. Visual Indicators and Metrics

A. Confidence Scores

Display Format:
(Confidence: 89%)
(100% match)
({confidence}% match)

Usage:
- Fuzzy matching results
- Database validation
- OCR accuracy indication

Visual Treatment:
- Parenthetical display
- Percentage format
- Inline with results

B. Count Metrics

Display Format:
Found 5 medicine(s)
2 warning(s)
3 potential interaction(s)

Usage:
- Result summaries
- Warning counts
- Interaction counts

Visual Treatment:
- Inline with headers
- Clear numerical display
- Contextual information

C. Progress Indicators

Loading Spinners:
with st.spinner("🔍 Analyzing symptoms..."):
    analysis = analyzer.analyze_symptoms(symptoms)

with st.spinner("🤖 AI is parsing medicine information..."):
    structured_data = ocr_engine.extract_structured_data(raw_text)

with st.spinner("🔍 Calculating risk score..."):
    risk_assessment = risk_engine.calculate_risk_score(...)

Features:
- Emoji indicators
- Action descriptions
- User feedback
- Professional appearance

4. Expandable Sections

Purpose: Progressive disclosure of detailed information

Implementation Pattern:
with st.expander("📄 View Raw Extracted Text"):
    st.text(raw_text)

with st.expander(f"Medicine {idx}: {med.get('name', 'Unknown')}"):
    # Medicine details

with st.expander(f"⚠️ {med_name.title()} - {len(warnings)} warning(s)"):
    # Warning details

with st.expander("🔍 View Calculation Details"):
    # Calculation breakdown

Benefits:
- Reduces visual clutter
- Optional detail viewing
- Better information hierarchy
- User control over detail level

Usage Locations:
- Raw OCR text
- Medicine details
- Individual warnings
- Calculation details
- Technical information

5. Structured Layouts

A. Column Layouts

Two-Column Display:
col1, col2 = st.columns(2)
with col1:
    st.write(f"Name: {med.get('name', 'Unknown')}")
    st.write(f"Form: {med.get('form', 'Unknown')}")
with col2:
    st.write(f"Active Salt: {med.get('active_salt', 'Unknown')}")
    st.write(f"Dosage: {med.get('dosage', 'Unknown')}")

Benefits:
- Efficient space usage
- Parallel information
- Better readability
- Organized presentation

Three-Column Display (Risk Score):
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    st.error(f"{risk_score}%")
    st.error(f"{risk_level} RISK")

Benefits:
- Center alignment
- Prominent display
- Visual focus
- Professional appearance

B. Section Separators

Horizontal Rules:
st.markdown("")

Usage:
- Between major sections
- After analysis results
- Before disclaimers
- Visual organization

Benefits:
- Clear section breaks
- Visual hierarchy
- Better readability
- Professional appearance

6. Typography and Formatting

A. Headers

Hierarchy:
st.header("Section Title")           # Large
st.subheader("Subsection Title")     # Medium
st.markdown("Markdown Header")   # Customizable

Usage:
- Main section titles
- Subsection organization
- Result categories
- Clear structure

B. Text Formatting

Bold Text:
st.write(f"Medicine: {medicine_name}")
st.write(f"Severity: {severity}")

Emphasis:
- Important terms
- Labels
- Key information
- Status indicators

C. Lists

Bullet Points:
st.write("• Fever")
st.write("• Headache")
st.write("✓ Drink plenty of fluids")
st.write("🚨 Temperature >103°F")

Benefits:
- Clear itemization
- Easy scanning
- Visual organization
- Icon enhancement

7. Transparency and Traceability

A. Raw Data Display

OCR Raw Text:
with st.expander("📄 View Raw Extracted Text"):
    st.text(raw_text)

Purpose:
- Show original extraction
- Enable verification
- Build trust
- Transparency

B. Extraction Method Indicator

Display:
st.info(f"Extraction Method: {structured_data.get('extraction_method', 'Unknown')}")

Values:
- "AI (LLaMA 3)"
- "Basic Pattern Matching"
- "Rule-Based"

Purpose:
- Method transparency
- User awareness
- Trust building
- Quality indication

C. Calculation Details

Risk Score Breakdown:
with st.expander("🔍 View Calculation Details"):
    details = risk_assessment['calculation_details']
    st.write(f"Base Score: {details['base_score']}")
    st.write(f"Severity Factor: {details['severity_factor']}")
    st.write(f"Age Factor: {details['age_factor']}")
    st.write(f"Medical History Factor: {details['history_factor']}")
    st.write(f"Final Score: {risk_score}%")

Purpose:
- Transparent calculations
- Explainable AI
- User trust
- Educational value

8. Real-Time Feedback

A. Immediate Validation

Empty Input:
if analyze_button and symptoms:
    # Process
elif analyze_button:
    st.warning("Please describe your symptoms to get guidance.")

Benefits:
- Instant feedback
- Clear guidance
- No confusion
- Better UX

B. Processing Indicators

Loading States:
with st.spinner("🔍 Reading prescription..."):
    raw_text = ocr_engine.extract_text_from_pil(image)

Benefits:
- User awareness
- Prevents confusion
- Professional appearance
- Manages expectations

C. Success Confirmation

Completion Messages:
st.success("✅ Text extracted successfully!")
st.success(f"✅ Found {len(medicines)} medicine(s)")

Benefits:
- Positive reinforcement
- Clear completion
- User confidence
- Good UX

9. Educational Disclaimers

Standard Disclaimer Format:
st.info("📌 Disclaimer: This is an educational tool. Always consult healthcare professionals for medical advice.")

Variations by Context:

Medicine Interaction:
"This is an educational tool. Always consult healthcare professionals for medical advice."

Prescription OCR:
"This is an educational tool. OCR may have errors. Always verify with healthcare professionals."

Symptom Analysis:
"This is an educational tool only. Always consult healthcare professionals for medical diagnosis and treatment."

Emergency Risk:
"🚨 IMPORTANT: This is an educational risk assessment tool only. It does NOT replace professional medical evaluation. If you are experiencing a medical emergency, call 911 or your local emergency number immediately."

Placement:
- End of results section
- After recommendations
- Prominent display
- Always visible

Visual Treatment:
- Blue info box (standard)
- Red error box (emergency)
- Bold emphasis
- Emoji indicators

10. Responsive Design

A. Column Adaptation

Desktop:
- Multi-column layouts
- Side-by-side display
- Efficient space usage

Mobile:
- Automatic stacking
- Single column
- Vertical layout
- Touch-friendly

B. Text Wrapping

Long Text:
- Automatic wrapping
- Readable line length
- No horizontal scroll
- Responsive sizing

C. Image Display

Prescription Images:
st.image(image, caption="Uploaded Prescription", use_column_width=True)

Benefits:
- Responsive sizing
- Maintains aspect ratio
- Fits container
- Mobile-friendly

Performance Optimization

1. Efficient Rendering

Strategies:
- Conditional rendering (only show when data available)
- Progressive disclosure (expandable sections)
- Lazy loading (images, large data)
- Minimal re-renders

2. Data Formatting

Pre-processing:
- Format data before display
- Calculate metrics once
- Cache formatted results
- Efficient string operations

3. Visual Feedback

Loading Indicators:
- Show during processing
- Hide when complete
- Clear status
- Manages expectations

Testing and Validation

Output Display Testing:

Color-Coded Messages:
- ✅ Success messages display correctly
- ✅ Info messages show appropriate content
- ✅ Warning messages highlight concerns
- ✅ Error messages indicate critical issues

Structured Data:
- ✅ Medicine information formatted correctly
- ✅ Interaction warnings clear and readable
- ✅ Symptom guidance well-organized
- ✅ Risk scores prominently displayed

Visual Indicators:
- ✅ Confidence scores visible
- ✅ Count metrics accurate
- ✅ Loading spinners work
- ✅ Progress indicators clear

Expandable Sections:
- ✅ Expand/collapse functional
- ✅ Content displays correctly
- ✅ Icons appropriate
- ✅ Headers descriptive

Layouts:
- ✅ Column layouts responsive
- ✅ Separators visible
- ✅ Spacing appropriate
- ✅ Hierarchy clear

Typography:
- ✅ Headers sized correctly
- ✅ Bold text emphasized
- ✅ Lists formatted properly
- ✅ Readable fonts

Transparency:
- ✅ Raw data accessible
- ✅ Methods indicated
- ✅ Calculations shown
- ✅ Trust established

Disclaimers:
- ✅ Always visible
- ✅ Appropriately placed
- ✅ Clear messaging
- ✅ Prominent display

Responsive Design:
- ✅ Desktop layout optimal
- ✅ Mobile layout functional
- ✅ Text wraps correctly
- ✅ Images responsive

Known Limitations

Current Limitations:

1. Visualization
   - No charts or graphs
   - No interactive visualizations
   - Text-based only
   - Limited graphics

2. Export
   - No PDF export
   - No print formatting
   - No data download
   - Session-only results

3. Customization
   - Fixed color scheme
   - Standard layouts
   - Limited theming
   - Streamlit defaults

4. Advanced Features
   - No animations
   - No real-time updates
   - No collaborative features
   - No result sharing

Future Enhancements

Planned Improvements:

1. Advanced Visualizations
   - Risk score gauges
   - Interaction network graphs
   - Symptom severity charts
   - Timeline visualizations

2. Export Functionality
   - PDF report generation
   - Print-friendly views
   - Data export (CSV, JSON)
   - Email results

3. Enhanced Formatting
   - Custom themes
   - Brand colors
   - Advanced layouts
   - Rich media support

4. Interactive Features
   - Drill-down capabilities
   - Hover tooltips
   - Interactive charts
   - Real-time updates

Deliverables

1. Color-Coded Messages
   - Success (green)
   - Info (blue)
   - Warning (yellow)
   - Error (red)

2. Structured Data Display
   - Medicine interaction results
   - Prescription OCR output
   - Symptom analysis results
   - Side-effect analysis
   - Risk assessment display

3. Visual Indicators
   - Confidence scores
   - Count metrics
   - Loading spinners
   - Progress indicators

4. Expandable Sections
   - Raw data views
   - Medicine details
   - Warning information
   - Calculation details

5. Structured Layouts
   - Column layouts
   - Section separators
   - Visual hierarchy
   - Responsive design

6. Typography
   - Header hierarchy
   - Bold emphasis
   - List formatting
   - Readable fonts

7. Transparency Features
   - Raw data display
   - Method indicators
   - Calculation breakdowns
   - Traceability

8. Real-Time Feedback
   - Immediate validation
   - Processing indicators
   - Success confirmation
   - Error messages

9. Educational Disclaimers
   - Context-appropriate
   - Prominently placed
   - Clear messaging
   - Always visible

10. Documentation
    - This activity documentation
    - Display patterns
    - Best practices
    - Testing results
