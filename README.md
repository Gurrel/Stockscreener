<body>
  <h1>Stock Screener</h1>
  <p><em>A real-time stock screener with trend analysis, order flow insights, and automated ticker detection.</em></p>

  <!-- Center the image and set width to 600px -->
  <div align="center">
    <img src="https://github.com/user-attachments/assets/7252ce67-507b-49ce-97cb-e6ddda1bf092" alt="stockscreener" width="400">
  </div>


  <h2>Features</h2>
  <ul>
    <li><strong>Real-time Stock Data</strong>: Fetches live stock quotes, price trends, and technical indicators.</li>
    <li><strong>Order Flow Analysis</strong>: Identifies key demand/supply zones and VWAP positions.</li>
    <li><strong>OCR-Based Ticker Recognition</strong>: Extracts stock tickers from screenshots.</li>
    <li><strong>Automated Trend Detection</strong>: Tracks EMAs (20, 50, 200), VWAP trends, structural trends, and demand/supply zones.</li>
    <li><strong>Historical Bar Analysis</strong>: Analyzes previous candle data to determine intra-bar price range insights.</li>
    <li><strong>Efficient Multithreading</strong>: Uses threading and multiprocessing to fetch and process data concurrently.</li>
    <li><strong>Interactive GUI</strong>: Displays data in an intuitive, real-time Tkinter-based interface.</li>
  </ul>

  <h2>Demo</h2>
  <a href="https://github.com/user-attachments/assets/a4832bc3-359a-4bae-9f09-b080a728d350">
    <img src="https://github.com/user-attachments/assets/your-thumbnail-image.png" alt="Watch the video" width="600">
  </a>



  


  <h2>How It Works</h2>
  <ol>
    <li><strong>Select a Region</strong>: Use the OCR-based feature to select a region on your screen for ticker detection.</li>
    <li><strong>Fetch Data</strong>: The application fetches real-time stock data for the detected ticker.</li>
    <li><strong>Display Data</strong>: Key indicators like VWAP, EMA, structural trends, and demand/supply zones update dynamically.</li>
    <li><strong>View in GUI</strong>: Data is presented in the Tkinter-based GUI.</li>
  </ol>

  <h2>Technologies Used</h2>
  <ul>
    <li><strong>Python</strong> – Core programming language.</li>
    <li><strong>Tkinter</strong> – GUI framework.</li>
    <li><strong>Multiprocessing &amp; Threading</strong> – For efficient background data fetching.</li>
    <li><strong>OCR (Tesseract or OpenCV)</strong> – For ticker extraction from screenshots.</li>
    <li><strong>Market Data App API</strong> – To retrieve real-time stock data.</li>
  </ul>

  <h2>Installation</h2>
  <h3>Clone the Repository</h3>
  <pre><code>git clone https://github.com/Gurrel/market-radar.git
cd market-radar</code></pre>

  <h3>Set Up a Virtual Environment</h3>
  <pre><code>python -m venv venv</code></pre>
  <p>Activate the virtual environment:</p>
  <ul>
    <li>On macOS/Linux: <code>source venv/bin/activate</code></li>
    <li>On Windows: <code>venv\Scripts\activate</code></li>
  </ul>

  <h3>Run the Application</h3>
  <pre><code>python main.py</code></pre>

  <h2>API Integration</h2>
  <p>This software uses the <a href="https://www.marketdata.app/">Market Data App API</a> to retrieve real-time stock data. Be sure to replace the API key in <code>main.py</code>:</p>
  <pre><code>API_KEY = "your_api_key_here"</code></pre>

  <h2>Tesseract OCR Installation</h2>
  <p>The application uses Tesseract OCR to perform ticker recognition. Please install Tesseract OCR before running the application.</p>
  <h3>Windows</h3>
  <p>Download and install Tesseract OCR from <a href="https://github.com/UB-Mannheim/tesseract/wiki">this link</a>. By default, it installs to:</p>
  <pre><code>C:\Program Files\Tesseract-OCR\tesseract.exe</code></pre>
  <p>Ensure that the path in <code>ocr_handling.py</code> is set correctly:</p>
  <pre><code>pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'</code></pre>
  
  <h3>Linux</h3>
  <p>On Ubuntu or Debian-based systems, install Tesseract with:</p>
  <pre><code>sudo apt-get update
sudo apt-get install tesseract-ocr</code></pre>
  
  <h3>macOS</h3>
  <p>If you use Homebrew, install Tesseract with:</p>
  <pre><code>brew install tesseract</code></pre>

<h2>License</h2>
<p>Copyright © 2025 Gustav Lundborg. All rights reserved.</p>
<p>This project is proprietary and confidential. No part of this project may be reproduced, distributed, or transmitted in any form or by any means, including photocopying, recording, or other electronic or mechanical methods, without the prior written permission of the copyright holder.</p>

  <h2>Contact</h2>
  <p>
    For questions or feedback, please reach out at
    <a href="mailto:gurre3@gmail.com">gurre3@gmail.com</a>
    or visit our
    <a href="https://github.com/Gurrel/market-radar/discussions">GitHub Discussions</a>.
  </p>
</body>

