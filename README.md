<!DOCTYPE html>
<html>
<head>
  <style>
    body {
      font-family: Roboto, Arial, sans-serif;
      font-size: 16px;
      color: #333333;
    }

    h2 {
      font-family: Roboto, Arial, sans-serif;
      font-size: 24px;
      color: #008080;
      font-weight: bold;
      margin-top: 20px;
      margin-bottom: 10px;
      text-decoration: underline;
    }

    p {
      font-family: Roboto, Arial, sans-serif;
      font-size: 16px;
      margin-bottom: 10px;
    }

    ul {
      font-family: Roboto, Arial, sans-serif;
      font-size: 16px;
      margin-bottom: 10px;
    }

    ol {
      font-family: Roboto, Arial, sans-serif;
      font-size: 16px;
      margin-bottom: 10px;
    }

    code {
      font-family: Consolas, Monaco, monospace;
      font-size: 14px;
    }
  </style>
</head>

<body>
  <h2>Data Export and Scheduling Tool</h2>
  <p>
    The Data Export and Scheduling Tool is a professional command-line utility designed to facilitate data export from databases to multiple formats (including CSV, XLSX, and JSON) and enable scheduled recurring exports. It offers users a convenient solution for automating data exports from both database tables and queries, providing flexibility in export customization and the ability to manage multiple export tasks simultaneously.
  </p>

  <h2>Table of Contents</h2>
  <ul>
    <li><a href="#project-description">Project Description</a></li>
    <li><a href="#project-structure">Project Structure</a></li>
    <li><a href="#installation">Installation</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#exporting-data">Exporting Data</a></li>
    <li><a href="#scheduling-runs">Scheduling Runs</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
  </ul>

  <h2 id="project-structure">Project Structure</h2>
  <p>
    The project structure is designed to promote maintainability and extensibility. This section provides an overview of the directories and files within the project, highlighting their roles and functionalities.
  </p>
  <ul>
    <li><code>core/</code>: This directory encompasses the core functionalities of the tool, including database functions 
        and data export logic. It serves as the foundation for the tool's operations.</li>
    <li><code>scheduler/</code>: The scheduler directory is responsible for managing the scheduling of data exports at 
        specified times. It plays a crucial role in automating the export process.</li>
    <li><code>scheduler/interface/</code>: This directory contains user interface modules that facilitate interaction 
        with the scheduler. It provides a user-friendly interface for configuring export times, selecting tables/queries, 
        and choosing export formats.</li>
    <li><code>core/export_data.py</code>: This file implements the data export functionality, enabling users to export 
        data to different file formats such as CSV, XLSX, and JSON. It encapsulates the logic required for exporting 
        data effectively.</li>
    <li><code>core/db_functions.py</code>: Within this file, you'll find functions that facilitate interaction with the 
        database. It enables the retrieval of preset queries and the fetching of available tables, enhancing the 
        flexibility of data exports.</li>
    <li><code>scheduler/schedule_user_interface.py</code>: This file encompasses user interface functions specifically 
        designed for prompting export times, table selections, and export formats. It ensures a seamless and intuitive 
        user experience during the scheduling process.</li>
    <li><code>main.py</code>: Serving as the main entry point of the tool, this file initiates the export and scheduling 
        processes. It brings together the core functionalities and orchestrates the execution of data exports and 
        scheduled runs.</li>
    <li><code>README.md</code>: This file serves as a comprehensive guide, providing an overview of the project, 
        installation instructions, usage guidelines, and other relevant information. It acts as a central source of 
        documentation and is essential for understanding the tool's features and how to effectively utilize them.</li>
  </ul>

  <h2 id="installation">Installation</h2>
  <p>
    Learn how to install the Data Export and Scheduling Tool on your system. This section provides step-by-step 
    instructions for installing the tool, ensuring a smooth setup process.
  </p>
  <ol>
    <li><b>Navigate to the project directory</b>: Open your command-line interface and navigate to the directory where the Data 
        Export and Scheduling Tool is located. For example, if the tool is stored in a directory named data-export-tool, 
        use the following command: <code>cd data-export-tool</code></li>
    <li><b>Install the dependencies</b>: The tool relies on certain dependencies to function properly. To install these 
        dependencies, use the following command: <code>pip install -r requirements.txt</code> <br>This command will read the 
        <code>requirements.txt</code> file, which contains a list of all the required packages and their versions. It will 
        automatically download and install the necessary dependencies for the tool.<br>
        <b>Note</b>: Make sure you have Python and pip installed on your system before running the above command.</li>
  </ol>
  <p>
   By following these steps, you can successfully install the Data Export and Scheduling Tool on your system. 
   Ensure that the installation process completes without any errors before proceeding to the next steps.
  </p>

  <h2 id="usage">Usage</h2>
  <p>
    Discover how to effectively use the Data Export and Scheduling Tool. This section provides a step-by-step guide to 
    configure the tool, run it, and interact with its features.
  </p>
  <ol>
    <li><b>Configure the database connection and preset queries</b>: Open the <code>core/db_functions.py</code> file and 
        configure the database connection settings according to your database setup. Additionally, you can define preset 
        queries or customize existing ones based on your requirements. This step ensures that the tool can access the 
        database and retrieve the necessary data for exporting.</li>
    <li><b>Run the tool</b>: Open your command-line interface and navigate to the project directory containing the Data 
        Export and Scheduling Tool. Use the following command to run the tool:<code>python main.py</code><br>
        This command will initiate the tool and display the user interface in the command-line interface.</li>
    <li>Follow the on-screen prompts to specify the export times, select tables/queries, and choose the export format.</li>
    <li>The tool will export the selected data to separate files and schedule the exports at the specified times. 
        The exported files will be stored in the specified export format (CSV, XLSX, or JSON).</li>
    <li><b>Automatic scheduled runs</b>: The tool will automatically execute the scheduled exports at the specified 
        times. It will continue running in the background, ensuring the timely execution of the scheduled tasks.</li>
    <li><b>Stopping the tool</b>: o stop the tool and halt the scheduled runs, press <strong>Ctrl + C</strong> in the 
        command-line interface. This will gracefully terminate the tool and prevent further scheduled exports.</li>
  </ol>

  <h2 id="exporting-data">Exporting Data</h2>
  <p>
    Master the process of exporting data using the tool. This section provides detailed instructions on exporting data 
    from saved queries, custom queries, and update queries. Learn how to select tables/queries, choose export formats, 
    and generate separate files for each export.
  </p>
  <ol>
    <li><b>Select the export type</b>: When prompted by the tool, choose the type of export you want to perform. You can select 
    from the following options:
        <ul>
            <li>Saved queries: Select from a list of pre-defined queries that have been saved in the tool.</li>
            <li>Custom queries: Specify your own custom queries to export data based on your specific requirements.</li>
            <li>Update queries: Choose update queries that modify the data in the database.</li>
        </ul>
    </li>
    <li><b>Select tables/queries</b>: After selecting the export type, the tool will prompt you to select the tables or queries 
        you want to export. Enter the numbers of the tables or queries separated by commas. For example, if you want to 
        export tables 1, 3, and 5, enter <code>1,3,5</code>.</li>
    <li>Choose the export format by entering the corresponding number. Available formats: 1. CSV, 2. XLSX, 3. JSON.</li>
    <li>The tool will now export the selected tables/queries to separate files in the chosen format. Each table/query 
        will generate a separate file containing the exported data. </li>
  </ol>

  <h2 id="scheduling-runs">Scheduling Runs</h2>
  <p>
    Learn how to schedule recurring data exports with ease. This section guides you through the process of specifying export times, selecting tables/queries to schedule, choosing export formats, and running automated exports at the scheduled times.
  </p>
  <ol>
    <li>When prompted, enter the export times in <code>HH:MM</code> format. You can enter multiple export times,
        separated by commas. For example, to schedule exports at 10:00 AM and 2:00 PM, enter <code>10:00,14:00</code>.</li>
    <li>Select the tables/queries you want to schedule. Enter the numbers of the tables/queries separated by commas.</li>
    <li>Choose the export format as mentioned in the "Exporting Data" section.</li>
    <li>The tool will schedule the exports for the selected tables/queries at the specified times. The exports will run 
        automatically at the scheduled times.</li>
    <li>The tool will continue running in the background and execute the scheduled exports at the specified times until 
        stopped manually (by pressing <strong>Ctrl + C</strong>).</li>
  </ol>

  <h2 id="contributing">Contributing</h2>
  <p>
    Contributions to the Data Export and Scheduling Tool are welcome! If you have any ideas, suggestions, or bug reports, 
    please open an issue or submit a pull request. When contributing, please follow the existing code style and ensure 
    that your changes are well-tested.

  <h2 id="license">License</h2>
  <p>
    The Data Export and Scheduling Tool is licensed under the <a href="./LICENSE" download>MIT License</a>. Click 
    <a href="./LICENSE" download>here</a> to download the license file.
  </p>

</body>
</html>