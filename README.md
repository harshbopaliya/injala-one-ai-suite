# Injala One AI Suite

🤖 **Intelligent Multi-Agent Document Analysis Platform**

A powerful Streamlit-based application that automatically selects and deploys specialized AI agents to analyze PDF documents based on your queries. The system intelligently routes requests to the most appropriate agent for optimal results.

## 🌟 Features

- **Intelligent Agent Auto-Selection**: Automatically detects the best AI agent for your specific query
- **Multi-Agent Architecture**: Six specialized agents for different document analysis tasks
- **PDF Processing**: Upload and analyze 1-2 PDF documents simultaneously
- **Gemini AI Integration**: Powered by Google's Gemini LLM for advanced natural language processing
- **Structured Output**: Get formatted, downloadable reports from agent analysis
- **User-Friendly Interface**: Clean Streamlit web interface with real-time processing

## 🏗️ Architecture

```
injala-one-ai-suite/
│
├── app.py                   # Streamlit front-end for the multi-agent pipeline
├── model_utils.py           # Gemini LLM loader utility
├── auto_router.py           # Agent auto-detection logic
├── asuretify.py             # AsuretifyAgent
├── kinetic.py               # KineticAgent
├── wrappotal.py             # WrappotalAgent
├── riskguru.py              # RiskguruAgent
├── prequaligy.py            # PrequaligyAgent
├── anzenn.py                # AnzennAgent
├── ocr_utils.py             # OCR + PDF extraction helpers
├── requirements.txt         # Dependencies
└── README.md                # Project documentation
```

## 🤖 Available Agents

| Agent | Purpose | File Count | Specialization |
|-------|---------|------------|----------------|
| **AsuretifyAgent** | Insurance compliance analysis | 2 files | Contract vs COI comparison |
| **KineticAgent** | Dynamic document processing | 1 file | Motion/workflow analysis |
| **WrappotalAgent** | Document wrapping & summarization | 1 file | Content consolidation |
| **RiskguruAgent** | Risk assessment & analysis | 1 file | Risk evaluation |
| **PrequaligyAgent** | Pre-qualification processing | 1 file | Eligibility assessment |
| **AnzennAgent** | Security & compliance analysis | 1 file | Security evaluation |

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Streamlit
- Google Gemini API Key
- Required Python packages (see `requirements.txt`)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/harshbopaliya/injala-one-ai-suite.git
   cd injala-one-ai-suite
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Get your Gemini API Key**
   - Visit [Google AI Studio](https://aistudio.google.com/)
   - Create a new API key
   - Keep it secure for use in the application

### Running the Application

1. **Start the Streamlit app**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser**
   - Navigate to `http://localhost:8501`
   - The application will load automatically

## 📖 Usage Guide

### Step 1: API Key Setup
- Enter your Gemini API key in the secure input field
- The key is required for all LLM operations

### Step 2: Upload Documents
- Upload 1-2 PDF files using the file uploader
- Supported format: PDF only
- File size limits apply based on your system

### Step 3: Enter Your Query
- Type your question or analysis request
- Be specific about what you want to analyze
- Examples:
  - "Compare contract vs COI for insurance compliance"
  - "Analyze risk factors in this document"
  - "Evaluate pre-qualification requirements"

### Step 4: Processing
- The system will automatically:
  - Analyze your query
  - Select the most appropriate agent
  - Process your documents
  - Generate structured output

### Step 5: Review Results
- View the analysis results in the output area
- Download the report as a text file if needed

## 🔧 Configuration

### Agent Selection Logic
The system uses intelligent routing based on:
- Query content analysis
- Document type detection
- Agent specialization matching
- Required file count validation

### File Requirements
- **Single File Agents**: Kinetic, Wrappotal, Riskguru, Prequaligy, Anzenn
- **Multi-File Agents**: Asuretify (requires 2 files)

## 🛠️ Development

### Adding New Agents

1. **Create agent file** (e.g., `newagent.py`)
   ```python
   class NewAgent:
       def __init__(self, model):
           self.model = model
       
       def run(self, *file_bytes):
           # Agent logic here
           return "Analysis result"
   ```

2. **Register in app.py**
   ```python
   from newagent import NewAgent
   
   AGENTS = {
       # ... existing agents
       "newagent": {"class": NewAgent, "file_count": 1},
   }
   ```

3. **Update auto_router.py** to include new agent detection logic

### Customizing OCR Processing
- Modify `ocr_utils.py` for custom PDF extraction
- Add support for different document formats
- Implement specialized text preprocessing

## 📋 Dependencies

Key packages required:
- `streamlit` - Web interface
- `google-generativeai` - Gemini AI integration
- `PyPDF2` or `pdfplumber` - PDF processing
- `pillow` - Image processing
- Additional dependencies in `requirements.txt`

## ⚠️ Important Notes

### Security
- API keys are handled securely through Streamlit's password input
- No keys are stored persistently in the application
- Always use environment variables in production

### Limitations
- File size limits depend on Streamlit and Gemini API constraints
- PDF processing may vary based on document complexity
- Agent selection accuracy depends on query clarity

### Error Handling
- Comprehensive error messages for troubleshooting
- Graceful handling of API failures
- File upload validation and feedback

## 🤝 Contributing

1. Fork the repository from [https://github.com/harshbopaliya/injala-one-ai-suite](https://github.com/harshbopaliya/injala-one-ai-suite)
2. Create a feature branch
3. Implement your changes
4. Add appropriate tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

## 🆘 Support

For issues, questions, or feature requests:
- Create an issue in the [GitHub repository](https://github.com/harshbopaliya/injala-one-ai-suite/issues)
- Check existing documentation
- Review error messages for troubleshooting hints

## 🔮 Future Enhancements

- Support for additional document formats
- Real-time collaboration features
- Advanced analytics and reporting
- Integration with cloud storage services
- Multi-language support

---

**Built with ❤️ using Streamlit and Google Gemini AI**