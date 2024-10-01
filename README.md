# Integrated Corporate Application - Distributor Module

Welcome to the Distributor Module of our integrated corporate application! This project is designed to streamline operations and enhance the efficiency of distributor management within a corporate ecosystem. The application encompasses three key themes: Retail, Supplier, and Distributor. This README will guide you through the project's purpose, features, setup instructions, and usage.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

The Distributor module serves as a crucial component of our corporate application, facilitating the management of distributor relationships, shipping logistics, and pricing estimates. It aims to provide a seamless user experience for distributors and enables efficient tracking and management of shipping operations.

## Features

- **Distributor Management**: Add, edit, and delete distributor records, including details such as city of origin and destination, shipping weight, and price estimates.
- **Dynamic Shipping Cost Calculation**: Calculate shipping costs based on the selected origin and destination cities, accounting for varying weights and distances.
- **User-Friendly Interface**: A responsive design utilizing Tailwind CSS to ensure an optimal experience across devices.
- **Data Validation**: Ensure accurate data entry through validation checks when submitting distributor information.
- **Interactive Pop-Ups**: Confirm actions such as deletion or editing with interactive pop-ups for a better user experience.
- **Search Functionality**: Quickly search for specific distributor records within the table.

## Technologies Used

- **Python**: Backend development using Python.
- **Flask**: A lightweight web framework for building web applications.
- **Firebase**: For database interactions, providing real-time updates and data storage.
- **HTML/CSS**: Structure and style the web application.
- **JavaScript**: Enhance interactivity and dynamic features on the frontend.
- **Tailwind CSS**: A utility-first CSS framework for responsive design.

## Setup Instructions

To set up the project locally, follow these steps:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/yourrepository.git
   cd yourrepository

2. **Create a Virtual Environment (recommended)**:

   ```bash
   python -m venv myenv
   source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`

3. **Install Dependencies**:

   Make sure you have requirements.txt that lists all the necessary packages. You can install them using:
   ```bash
   pip install -r requirements.txt

4. **Set Up Firebase**:

- Create a Firebase project and set up Firestore or Realtime Database as needed.
- Update the Firebase configuration in your application to connect to your database.


5. **Run the Application**:

   ```bash
   python app.py

The application should now be running on http://localhost:5000 (or the specified port).

## Usage

Upon running the application, users can navigate to the distributor module, where they can:

- Add Distributors: Fill out the form to add new distributor details.
- Edit Distributor Records: Click on the edit button next to a record to update details.
- Delete Distributor Records: Use the delete button to remove a distributor, with a confirmation pop-up to prevent accidental deletions.
- Calculate Shipping Costs: Enter the origin city, destination city, and weight to receive an estimated shipping cost.
- Search for Distributors: Utilize the search feature to quickly find specific distributors in the list.

## Contributing

Contributions are welcome! If you would like to contribute to this project, please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Make your changes and commit them.
4. Push your branch to your forked repository.
5. Create a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

Thank you for exploring the Distributor Module of our integrated corporate application! For any inquiries or feedback, please feel free to reach out.

Feel free to customize any sections as needed!

# Distributor 6 API Documentation

## Accessing the Website
The Distributor 6 system can be accessed through the following link:
[http://159.223.41.243:8000](http://159.223.41.243:8000)

Users can use this system to retrieve shipping cost information and track the shipment status.

## API Endpoints

1. **[ENDPOINT]** `GET /api/distributors6`
**Get Distributor Information**:
This endpoint is used to retrieve general information about the distributor, such as shipping cost per kilogram, origin city, destination city, and estimated delivery time.

   ```bash
   [
    {
        "harga_ongkir_per_kg": 960,
        "id_distributor": 6,
        "kota_asal": "bandung",
        "kota_tujuan": "bali",
        "lama_pengiriman": "5 hari"
    },
    {
        "harga_ongkir_per_kg": 840,
        "id_distributor": 6,
        "kota_asal": "bandung",
        "kota_tujuan": "ngawi",
        "lama_pengiriman": "5 hari"
    }
   ]

2. **[ENDPOINT]** `POST /api/distributors6/orders/cek_ongkir`
**Check Shipping Cost (Without Purchase Confirmation)**:
Suppliers can use this endpoint to check the shipping cost without having to confirm the purchase.

   
   ```json
   #Example Input:
   {
       "id_log": 102,
       "kota_asal": "Semarang",
       "kota_tujuan": "Surabaya",
       "berat": 5
   }


   #Example Response:
   {
    "harga_pengiriman": 4200.0,
    "id_log": 102,
    "lama_pengiriman": "4 hari"
   }


3. **[ENDPOINT]** `POST /api/distributors6/orders/fix_kirim`
**Confirm Shipment**:
This endpoint is accessed by the supplier when the retail has decided to purchase the product and use Distributor 6's service for the shipment.

   ```bash
   #Example Input:
   {
    "id_log": 800
   }

   #Example Response:
   {
    "harga_pengiriman": 40000,
    "id_log": 800,
    "lama_pengiriman": "10 hari",
    "no_resi": "JJ2Q2H5UDV",
    "tanggal_pembelian": "2024-09-28"
   }



4. **[ENDPOINT]** `GET /api/status/<string:no_resi>`
**Track Shipment Status**:
Retailers can use this endpoint to track the status of the shipment by entering the shipping tracking number.

   **Example Request**
   'GET /api/status/JJ2Q2H5UDV'
   
   ```bash
   #Example Response:
   {
    "lama_pengiriman": "4 hari",
    "status": "On Progress"
   }

