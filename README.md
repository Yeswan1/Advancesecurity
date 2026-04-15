# 👋 Hi, Yeswanth surya raj
# 🔐 Network Security Prediction using Machine Learning

This project is a **Streamlit web application** that predicts **network security threats** using a trained ML model.  
It allows users to upload CSV data, run predictions, and download results.

🌍 **Live App:** [Network Security Checker](https://security-clou.onrender.com/)

---

## 📌 Features
- Upload CSV file for network traffic/security data
- Preprocessing & ML model prediction
- Interactive UI built with Streamlit
- Save predictions to `prediction_output/`
- Download predictions as CSV
- MongoDB integration for storing/reading data

---

## 📥 Input Features  

The model expects the following features in the CSV file:  

| Feature Name                 | Description                                                                 |
|-------------------------------|-----------------------------------------------------------------------------|
| `having_IP_Address`          | 1 if the URL contains an IP address, -1 otherwise                          |
| `URL_Length`                 | Length of the URL (1=legit, -1=suspicious)                                 |
| `Shortining_Service`         | 1 if using a shortening service (e.g., bit.ly), -1 otherwise               |
| `having_At_Symbol`           | 1 if `@` symbol exists in URL, -1 otherwise                                |
| `double_slash_redirecting`   | Checks for `//` redirection in URL                                          |
| `Prefix_Suffix`              | 1 if prefix/suffix separated by `-` in domain, -1 otherwise                 |
| `having_Sub_Domain`          | Number of subdomains (1=legit, 0=suspicious, -1=phishing)                  |
| `SSLfinal_State`             | 1 if SSL certificate is valid, -1 otherwise                                |
| `Domain_registeration_length`| Domain validity duration                                                    |
| `Favicon`                    | Whether favicon is loaded from same domain                                  |
| `port`                       | 1 if standard ports used, -1 if unusual                                     |
| `HTTPS_token`                | 1 if `https` token appears in URL, -1 otherwise                            |
| `Request_URL`                | % of external objects loaded (1=low, -1=high)                              |
| `URL_of_Anchor`              | % of suspicious anchor links                                               |
| `Links_in_tags`              | % of suspicious links in `<meta>`, `<script>`, etc.                        |
| `SFH`                        | Server Form Handler (1=legit, -1=phishing)                                 |
| `Submitting_to_email`        | 1 if form submission goes to email, -1 otherwise                           |
| `Abnormal_URL`               | 1 if abnormal structure, -1 otherwise                                      |
| `Redirect`                   | Number of redirects                                                        |
| `on_mouseover`               | 1 if status bar changes on hover                                           |
| `RightClick`                 | 1 if right-click disabled                                                  |
| `popUpWidnow`                | 1 if pop-up windows present                                                |
| `Iframe`                     | 1 if iframe present                                                        |
| `age_of_domain`              | Domain age                                                                 |
| `DNSRecord`                  | 1 if DNS record exists, -1 otherwise                                       |
| `web_traffic`                | Website traffic rank                                                       |
| `Page_Rank`                  | Google PageRank score                                                      |
| `Google_Index`               | 1 if indexed by Google, -1 otherwise                                       |
| `Links_pointing_to_page`     | Number of external links pointing                                           |
| `Statistical_report`         | 1 if domain/IP found in suspicious reports, -1 otherwise                   |

📌 The dataset may also include `predicted_column` if predictions were saved earlier.  

---

## 📊 Input Example  

Example `input.csv` file:  

| having_IP_Address | URL_Length | Shortining_Service | having_At_Symbol | double_slash_redirecting | Prefix_Suffix | having_Sub_Domain | SSLfinal_State | Domain_registeration_length | Favicon | port | HTTPS_token | Request_URL | URL_of_Anchor | Links_in_tags | SFH | Submitting_to_email | Abnormal_URL | Redirect | on_mouseover | RightClick | popUpWidnow | Iframe | age_of_domain | DNSRecord | web_traffic | Page_Rank | Google_Index | Links_pointing_to_page | Statistical_report |
|-------------------|------------|--------------------|------------------|--------------------------|---------------|-------------------|----------------|-----------------------------|---------|------|-------------|-------------|---------------|---------------|-----|---------------------|--------------|----------|--------------|------------|-------------|--------|---------------|-----------|-------------|-----------|--------------|------------------------|-------------------|
| 1                 | -1         | 1                  | 1                | 1                        | -1            | 1                 | 1              | 1                           | 1       | 1    | -1          | -1          | 1             | 1             | 0   | 1                   | 1            | 0        | 1            | 1          | 1           | 1      | 1             | 1         | -1          | -1        | 1            | 1                      | 1                 |
| -1                | -1         | -1                 | 1                | -1                       | 1             | 1                 | 1              | -1                          | 1       | 1    | -1          | 1           | 1             | 0             | 1   | 1                   | -1           | 0        | 1            | 1          | 1           | 1      | -1            | -1        | 1           | 1         | -1           | 1                      | 1                 |

---

## 📤 Output Predictions  

After uploading, the model adds a `predicted_column` with results:  

- **1 → Legitimate Website**  
- **0 → Phishing Website**  

Example `output.csv`:  

| having_IP_Address | URL_Length | Shortining_Service | ... | Statistical_report | predicted_column |
|-------------------|------------|--------------------|-----|-------------------|------------------|
| 1                 | -1         | 1                  | ... | 1                 | 1.0 (Legitimate) |
| -1                | -1         | -1                 | ... | 1                 | 0.0 (Phishing)   |

✔️ Predictions are shown in the app and available for download as `predictions.csv`.  

---

"# Advancesecurity" 
