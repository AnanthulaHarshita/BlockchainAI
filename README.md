# AI with Ethereum Flask Web Application

This project demonstrates how to integrate Ethereum smart contracts with a Flask web application, enabling interaction with the Ethereum blockchain via **Ethers.js** and **Flask**. The system uses smart contracts to manage and verify the details of individuals who have been issued a visa. Additionally, the project includes a **dummy AI model** to predict visa issuances based on input features.

## Features

- **Flask Backend**: Interacts with Ethereum smart contracts to manage visa issuance data.
- **Ethers.js**: Uses Ethers.js for front-end blockchain interaction with MetaMask.
- **MetaMask**: Handles Ethereum wallet transactions and signing.
- **Simple Web Interface**: Built using HTML and JavaScript to interact with the smart contract.
- **Dummy AI Model**: Predicts the likelihood of visa issuance based on applicant data (e.g., nationality, age, occupation).

## Requirements

- **Python 3.x**
- **Node.js** (for Ethers.js)
- **MetaMask** (for wallet management)
- **Flask** & **Web3.py** (for backend)
- **Ethers.js** (for front-end)
- **Infura or Alchemy** for Ethereum node access
- **scikit-learn** (for machine learning model)
- **pandas** and **numpy** (for data processing)

## Steps to Set Up

1. **Install dependencies**:
   - Install Python packages:
     ```bash
     pip install Flask web3 scikit-learn pandas numpy
     ```
   - Install Node.js dependencies:
     ```bash
     npm init -y
     npm install ethers
     ```

2. **Flask Backend**:
   - In `app.py` (Flask backend), connect to Ethereum using **Infura** or **Alchemy** and serve the front-end HTML page.
   - The smart contract interacts with data about individuals who have been issued a visa, managing the storage and verification of these records on the Ethereum blockchain.

3. **Front-end**:
   - In `index.html`, use **Ethers.js** to interact with the Ethereum network via **MetaMask**.
   - The front-end allows users to input visa-related details and view whether their visa issuance is recorded on the blockchain.

4. **Deploy Your Smart Contract**:
   - Use **Remix IDE** to deploy your smart contract that manages visa issuance records on the blockchain. 
   - The smart contract will store records like the applicant’s name, nationality, and visa status.

5. **Dummy AI Model**:
   - The AI model simulates predictions for visa issuance based on factors like nationality, age, occupation, etc. The AI model can be trained on historical data and used to predict whether an applicant would be issued a visa.
   - This AI model does not interact with the smart contract but provides a separate functionality for predicting visa issuance.

6. **Run the Flask App**:
   ```bash
   python app/main.py
