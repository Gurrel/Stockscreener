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
    <li><strong>OCR-Based Ticker Recognition</strong>: Extracts stock tickers from automated screenshots.</li>
    <li><strong>Automated Trend Detection</strong>: Tracks EMAs (20, 50, 200), VWAP trends, structural trends, and demand/supply zones.</li>
    <li><strong>Historical Bar Analysis</strong>: Analyzes previous candle data to determine intra-bar price range insights.</li>
    <li><strong>Efficient Multithreading</strong>: Uses threading and multiprocessing to fetch and process data concurrently.</li>
    <li><strong>Interactive GUI</strong>: Displays data in an intuitive, real-time Tkinter-based interface.</li>
  </ul>

  <h2>Demo</h2>
  
  https://github.com/user-attachments/assets/b4eb59f3-3dd0-4fd4-b46b-25ee758da704

  <h2>How It Works</h2>
  <ol>
    <li><strong>Select a Region</strong>: Use the OCR-based feature to select a region on your screen for ticker detection.</li>
    <li><strong>Fetch Data</strong>: The application fetches real-time stock data for the detected ticker.</li>
    <li><strong>Process Data</strong>: After fetching, the application calculates key market indicators:
      <ul>
        <li><strong>VWAP (Volume-Weighted Average Price)</strong>:
          <ul>
            <li>Retrieves minute-by-minute price and volume data.</li>
            <li>Computes VWAP by weighting price by volume over time.</li>
            <li>Determines price position relative to VWAP (above/below) for trend analysis.</li>
          </ul>
        </li>
        <li><strong>EMA (Exponential Moving Averages)</strong>:
          <ul>
            <li>Calculates EMA for 20, 50, and 200 periods.</li>
            <li>Applies more weight to recent prices to detect momentum shifts.</li>
            <li>Compares short-term and long-term EMAs to identify trend direction.</li>
            <img src="https://github.com/user-attachments/assets/ada59473-cc90-44bc-83a5-f3f967619605" alt="EMA Example" width="500">
          </ul>
        </li>
        <li><strong>Structural Trends</strong>:
          <ul>
            <li>Analyzes daily, weekly, and monthly price trends.</li>
            <img src="https://github.com/user-attachments/assets/8089693f-fa6c-46dd-a484-03ee1fa28cf2" alt="Trend Example" width="500">
          </ul>
        </li>
        <li><strong>Demand & Supply Zones</strong>:
          <ul>
            <li>Detects significant price levels where strong buying or selling occurred.</li>
            <img src="https://github.com/user-attachments/assets/c660a377-d35c-4710-ac2a-d2a4de18793a" alt="Zones Example" width="500">
          </ul>
        </li>
        <li><strong>Previous Bar Analysis</strong>:
          <ul>
            <li>Retrieves high/low values of the previous bar (candle).</li>
            <li>Calculates whether the current price is inside or outside the previous bar’s range.</li>
            <li>Expresses relative position as a percentage.</li>
          </ul>
        </li>
      </ul>
    </li>
    <li><strong>Display Data</strong>: Processed insights update dynamically in the Tkinter GUI for real-time analysis.</li>
    <li><strong>View in GUI</strong>: The user interface displays stock trends, support zones, VWAP positions, and EMA crossovers in a structured format.</li>
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
  <p>The application uses Tesseract OCR to perform ticker recognition.</p>
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

<h2>Using TradingView for OCR-Friendly Ticker Display</h2>
<p>To enhance the accuracy of ticker recognition, you can use this Pine Script in <a href="https://www.tradingview.com/">TradingView</a>. This script displays the stock ticker in large, high-contrast text at the top right of the screen, making it easier for the OCR system to read.</p>

<h3>📜 Pine Script Code</h3>
<pre><code>// This Pine Script™ code is subject to the terms of the Mozilla Public License 2.0 at https://mozilla.org/MPL/2.0/
// © Gurrel
//@version=6
  
indicator("Display Ticker", overlay = true)
ticker = syminfo.ticker

var table ticker_table = table.new(position.top_right, 1, 1)
if barstate.islast
    table.cell(ticker_table, column = 0, row = 0, text = ticker, text_color = color.white, text_size = size.huge, bgcolor = #000000, text_font_family = font.family_monospace)
</code></pre>

<h3>🔧 How to Use It</h3>
<ol>
    <li>Open <a href="https://www.tradingview.com/">TradingView</a> and go to your stock chart.</li>
    <li>Click on <strong>Pine Editor</strong> at the bottom of the screen.</li>
    <li>Paste the script above into the editor.</li>
    <li>Click <strong>Add to Chart</strong> to display the stock ticker in large text.</li>
    <li>Use the OCR feature in the stock screener app to detect the ticker more accurately.</li>
</ol>

<p>With this script, the OCR tool in the stock screener will have an easier time recognizing the ticker symbol, reducing errors and improving the user experience.</p>

<h2>License</h2>
<p>Copyright © 2025 Gustav Lundborg. All rights reserved.</p>
<p>This project is proprietary. No part of this project may be reproduced or distributed in any form or by any means without the prior written permission of the copyright holder.</p>
<p>Large swaths of code has been <strong>REDACTED</strong> for this sole purpose.</p>

  <h2>Contact</h2>
  <p>
    For questions or feedback, please reach out at
    <a href="mailto:gurre3@gmail.com">gurre3@gmail.com</a>
  </p>
</body>

