# Training Feedback Survey App

A comprehensive Streamlit-based application for collecting and analyzing training feedback across multiple training courses with advanced data persistence, interactive visualizations, and professional user interface.

## 🚀 Quick Start

```bash
# Clone repository  
git clone https://github.com/wrightplace4solutions/survey-app-prototype-demo.git
cd survey-app-prototype-demo

# Setup environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run Home.py
```

## 📋 Features

### **Multi-Page Application**
- **Home Page**: Navigation hub with system overview and QR code integration
- **Survey Page**: Comprehensive training feedback collection interface
- **Results Dashboard**: Advanced analytics with interactive visualizations

### **Survey Collection**
- 5 Training sections: Title Class, FDRI/DLID, Driver Examiner, Compliance, Advanced VDH FDRII  
- Multiple question types: Skills priority, challenges, confidence ratings, expected improvements, audit issues
- Demographics collection with 14+ CSC locations
- Onboarding assessment including e-Learning and OJT evaluation
- Survey experience feedback and recommendations

### **Data Management**
- Dual persistence: CSV and Excel formats
- 42-column structured data schema
- Automatic file creation and column validation
- Comprehensive error handling and data integrity checks
- Unique submission tracking with timestamps

### **Analytics Dashboard**
- Interactive filtering by CSC location and date range
- Multiple visualization types: bar charts, pie charts, summary statistics
- Real-time data updates and responsive design
- Export capabilities for filtered data (CSV/Excel)
- Raw data table view with pagination

### **User Experience**
- Professional burgundy/tan color scheme
- Responsive layout with animated elements  
- Session state management across pages
- Form validation and progress indicators
- Success animations and clear feedback messages

## 📁 Project Structure

```
survey-app-prototype-demo/
├── Home.py                                          # Landing page & navigation
├── pages/
│   ├── 2_Survey.py                                 # Main survey interface
│   └── 3_Results.py                                # Analytics dashboard
├── assets/
│   ├── avatar_intro.mp4                            # Introduction video
│   ├── DMV New Logo.png                            # Application branding
│   └── survey_qr.png                               # QR code for mobile access
├── Updated_Training_Feedback_Survey_Template.csv   # Primary data storage
├── Updated_Training_Feedback_Survey_Template.xlsx  # Excel data backup
├── utils.py                                        # Shared utility functions  
├── requirements.txt                                # Python dependencies
├── README.md                                       # This documentation
└── FEATURES_LOG.md                                 # Complete feature documentation
```

## 🛠 Technical Requirements

- **Python**: 3.9 or higher
- **Dependencies**:
  - `streamlit>=1.28.0` - Web application framework
  - `pandas>=1.5.0` - Data manipulation and analysis
  - `openpyxl>=3.0.0` - Excel file handling
  - `altair>=4.2.0` - Interactive data visualizations

## 📊 Data Schema

The application collects 42 data points per submission:

- **Basic Info**: Submission ID, timestamp, demographics (name, role, CSC, email)
- **Training Feedback**: 5 sections × 5 questions each (25 total)
- **Onboarding Assessment**: Process description, coach assignment, support details  
- **E-Learning Evaluation**: Time allocation, challenges, barriers
- **OJT Assessment**: Success rates, completion factors
- **Survey Experience**: Rating, comments, recommendations

## 🎯 Use Cases

1. **Training Program Evaluation**: Assess effectiveness across different training modules
2. **CSC Performance Analysis**: Compare feedback across customer service centers
3. **Onboarding Process Improvement**: Identify gaps in new hire integration
4. **Skills Gap Analysis**: Understand priority skills and common challenges
5. **Quality Assurance**: Track audit issues and improvement areas

## 📈 Recent Improvements

- ✅ Fixed data persistence issues with column name standardization
- ✅ Added comprehensive error handling for file operations  
- ✅ Enhanced user interface with professional styling and animations
- ✅ Improved analytics dashboard with advanced filtering and export options
- ✅ Added missing e-Learning and OJT assessment capabilities
- ✅ Implemented session state management for better user experience

## 📚 Documentation

For complete feature documentation, implementation details, and customization guide, see [FEATURES_LOG.md](FEATURES_LOG.md).

## 🔗 Access

- **Local**: http://localhost:8501  
- **Survey Direct**: http://localhost:8501/2_Survey
- **Results Direct**: http://localhost:8501/3_Results

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/improvement`)  
5. Create Pull Request

## 📄 License

This project is licensed under the MIT License - see the repository for details.