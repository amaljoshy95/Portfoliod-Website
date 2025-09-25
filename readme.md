# Portfolioid

Portfolioid is a web application designed for users in India to track their mutual fund and equity investments through a paper trading platform. It allows users to simulate buying and selling stocks, maintain a history of transactions, and visualize their investment performance through charts.

## Features

- **User Authentication**: Secure signup and login system with password hashing.
- **Portfolio Tracking**: Monitor equity and mutual fund investments with real-time data integration.
- **Buy/Sell Simulation**: Perform paper trades to buy and sell stocks, with validation for prices, shares, and dates.
- **Transaction History**: View a detailed history of all transactions, sorted by date.
- **Performance Metrics**: Calculate metrics like CAGR (Compound Annual Growth Rate) and XIRR (Extended Internal Rate of Return) for investments.
- **Stock Search**: Search for stocks using the Yahoo Finance API.
- **Charts and Visualizations**: Display investment data through charts for better insights.
- **Responsive UI**: Templates for intuitive user interaction (e.g., `buy.html`, `sell.html`, `history.html`, `index.html`).

## Tech Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLite with tables for users, holdings, and transaction history
- **Frontend**: HTML templates with Jinja2, enhanced with JavaScript for dynamic interactions
- **APIs**: Yahoo Finance API for stock data retrieval
- **Security**: Password hashing with Werkzeug, session management for user authentication
- **Environment**: Managed using `python-dotenv` for secure configuration
- **Dependencies**: External libraries like `requests` for API calls and custom helpers for calculations

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/portfolioid.git
   cd portfolioid
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**:
   Create a `.env` file in the project root and add the Flask secret key:
   ```env
   FLASK_SECRET_KEY=your-secret-key
   ```

5. **Initialize the Database**:
   The application automatically creates a SQLite database (`users.db`) with the required tables (`users`, `holdings`, `history`) on startup.

6. **Run the Application**:
   ```bash
   python app.py
   ```
   The app will run on `http://0.0.0.0:5000` in debug mode.

   OR

   ```bash
   flask run
   ```
   The app will run on `localhost:5000` 

## Usage

1. **Signup/Login**: Create an account or log in to access the dashboard.
2. **Buy Stocks**: Navigate to the `/buy` route, enter stock details (symbol, price, shares, date), and submit to record a purchase.
3. **Sell Stocks**: Go to the `/sell` route, select a stock from your holdings, specify the sell price and shares, and confirm the transaction.
4. **View Portfolio**: The homepage (`/`) displays your current holdings, average purchase price, and performance metrics like XIRR.
5. **Transaction History**: Visit `/history` to see a chronological list of all buy/sell transactions.
6. **Search Stocks**: Use the `/search/<query>` endpoint to find stocks via Yahoo Finance API.
7. **Visualize Data**: Charts on the homepage provide insights into your portfolio's performance.

## Database Schema

- **users**: Stores user information (`id`, `username`, `hash`).
- **holdings**: Tracks current stock holdings (`id`, `symbol`, `shares`, `price`, `date`, `user_id`, `name`).
- **history**: Logs all transactions (`id`, `symbol`, `shares`, `price`, `date`, `user_id`, `name`, `ref_buy_date`, `type`).

## API Endpoints

- **GET /**: Displays the portfolio dashboard with holdings and performance metrics.
- **GET/POST /buy**: Handles stock purchase simulation.
- **GET/POST /sell**: Manages stock selling with profit and CAGR calculations.
- **GET /history**: Shows transaction history.
- **GET /search/<query>**: Searches for stocks using Yahoo Finance API.
- **GET /stock_detail_api/<symbol>/<view>**: Retrieves stock data for visualization.
- **GET/POST /login**: User login.
- **GET/POST /signup**: User registration.
- **GET /logout**: Clears session and logs out.

## Custom Functions

- **login_required**: Decorator to restrict access to authenticated users.
- **calc_xirr**: Calculates the Extended Internal Rate of Return for investments.
- **year_diff**: Computes the time difference between two dates for CAGR calculations.
- **get_stock_data**: Fetches stock data from external APIs (implementation in `get_stock_data.py`).
- **strptime_filter**: Custom Jinja2 filter for parsing dates in templates.

## Project Structure
```bash
portfolioid/
│── app.py                 # Main Flask app
│── helpers.py             # Utility functions (login_required, XIRR, CAGR, etc.)
│── get_stock_data.py      # Fetch stock/mutual fund data
│── users.db               # SQLite database (auto-created)
│── templates/             # HTML templates (login, signup, index, history, buy, sell)
│── static/                # Static assets (CSS, JS)
│── .env                   # Environment variables
│── requirements.txt       # Python dependencies
```

## Notes

- The application uses the `.NS` and `.BO` suffixes for Indian stock symbols (e.g., NSE and BSE), which are stripped during processing.
- Transactions are validated to ensure positive shares and prices.
- The SQLite database enforces foreign key constraints for data integrity.
- The app is designed for paper trading and does not involve real financial transactions.

## Future Improvements

- Add support for mutual fund-specific features (e.g., NAV tracking).
- Enhance charting with more interactive visualizations using libraries like Chart.js.
- Implement portfolio diversification analysis.
- Add support for multi-currency investments.
- Improve error handling and user feedback for invalid inputs.

## Contributing

Contributions are welcome! Please fork the repository, create a feature branch, and submit a pull request with your changes.

