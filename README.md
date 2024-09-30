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
