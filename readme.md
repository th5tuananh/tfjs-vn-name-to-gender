### tfjs-vn-name-to-gender

This is a Vietnamese name to gender prediction project that supports both **JavaScript (TensorFlow.js)** and **Python (TensorFlow/Keras)** implementations.

The goal is to predict gender based on Vietnamese names with 97% accuracy.

### 🌐 Web Version (JavaScript)
Open `index.html` in your browser to use the web interface.

### 🐍 Python Version (NEW!)
```bash
cd python
pip install -r requirements.txt
python predict.py --name "Nguyễn Văn Nam"
```

See [README-VI.md](README-VI.md) for detailed Vietnamese documentation.

### How it's made

1. Generate `dataset.csv` containing Name - Gender (63,773 Vietnamese names)
2. Train the model using TensorFlow/Keras - More details in `LSTM.ipynb`
3. Export models for both JavaScript and Python usage
4. Character-level tokenization for better accuracy

### Project Structure

```
📁 Repository/
├── 📁 python/              # Python implementation
│   ├── data_preprocessing.py
│   ├── train_model.py
│   ├── predict.py
│   └── requirements.txt
├── 📁 js/                  # JavaScript for web
├── 📁 models/              # Trained models
├── 📄 dataset.csv          # Training data
├── 📄 index.html           # Web interface
└── 📄 README-VI.md         # Vietnamese documentation
```

### Changelog

**v3.0**: Added Python implementation with TensorFlow/Keras
- Complete Python package with preprocessing, training, and prediction
- Vietnamese documentation
- Command-line interface
- Batch prediction support

**v2.0**: tokenize by character instead of word

**v1.0**: initial version, tokenize by word

### Author

* ngxson (Nui Nguyen)
* Email: contact at ngxson dot com
* My website: https://ngxson.com
