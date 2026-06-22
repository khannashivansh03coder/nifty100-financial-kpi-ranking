CREATE TABLE companies (
    id TEXT PRIMARY KEY,
    company_logo TEXT,
    company_name TEXT NOT NULL,
    chart_link TEXT,
    about_company TEXT,
    website TEXT,
    nse_profile TEXT,
    bse_profile TEXT,
    face_value REAL,
    book_value REAL,
    roce_percentage REAL,
    roe_percentage REAL
);
CREATE TABLE stock_prices (
    id INTEGER PRIMARY KEY,
    company_id TEXT NOT NULL,
    date TEXT NOT NULL,
    open_price REAL NOT NULL CHECK (open_price > 0),
    high_price REAL NOT NULL CHECK (high_price > 0),
    low_price REAL NOT NULL CHECK (low_price > 0),
    close_price REAL NOT NULL CHECK (close_price > 0),
    volume INTEGER NOT NULL CHECK (volume >= 0),
    adjusted_close REAL NOT NULL CHECK (adjusted_close > 0),

    FOREIGN KEY (company_id) REFERENCES companies(id)
);
