export const bio = [
  "Hello! Thank you for visiting my page. My name is <b>Jesse Anderson</b> and I have a passion for building engineering and automation tools to solve problems.",
  "Besides coding, I enjoy reading, woodworking, and climbing. Constantly expanding one's skillsets and learning by doing are central tenets in my life. I consider myself a lifelong learner, and every day presents a possibility to grow further. ",
  "Thanks for taking the time to learn a little about me!",
  "<em>**The projects are interactive! Click on any project to get directed to its page.**"
];

export const skills = [
  {
    title: "MATLAB",
    skillName: "MATLAB",
    color: "1",
    percentage: "90",
  },
  {
    title: "Python",
    skillName: "Python[scipy, scikitlearn, pandas, numpy, ...]",
    color: "2",
    percentage: "75",
  },
  {
    title: "Web",
    skillName: "HTML, CSS,Javascript",
    color: "4",
    percentage: "50",
  },
  {
    title: "R",
    skillName: "R",
    color: "6",
    percentage: "75",
  },
  {
    title: "Visual Basic, VBA",
    skillName: "Visual Basic, VBA, OLE Automation",
    color: "3",
    percentage: "80",
  },
  {
    title: "C++ & Julia",
    skillName: "C++, Julia",
    color: "5",
    percentage: "50",
  },
  {
    title: "Version Control",
    skillName: "GitHub, Git, Github Desktop",
    color: "7",
    percentage: "70",
  },
  {
    title: "Editors",
    skillName: "VS Code, Spyder, Jupyter",
    color: "1",
    percentage: "75",
  },
  {
    title: "Data Science",
    skillName: "Power BI, Tableau",
    color: "1",
    percentage: "60",
  },
];

export const projects = {
  disclaimer:
    "<em>***All the projects I listed were completed in an academic or research setting. As for my work in industry, many projects are proprietary and cannot be disclosed.***",
  
  mlProjects: [
    {
      projectName: "VAE-GAN",
      image: "images/GANOutput.png",
      summary:
        "Train a Variational AutoEncoder Generative Adversarial Network to generate images from the MNIST dataset prior to training a Denoising Autoencoder, Variational Autoencoder, and Generative Adversarial Network.",
      preview: "https://blog.jesse-anderson.net/posts/VAE_GAN/VAEGAN",
      techStack: ["Python","Cluster Analysis"],
    },
    {
      projectName: "Educational DBSCAN Tool",
      image: "images/DBSCAN_JS_Img.png",
      summary:
        "Javascript program which will perform DBSCAN clustering on various distributions in 2 dimensions.",
      preview: "https://blog.jesse-anderson.net/posts/DBSCAN/#conclusion",
      techStack: ["Javascript","Cluster Analysis", "DBSCAN","d3.v7.js"],
    },
    {
      projectName: "Python Clustering Toolbox",
      image: "images/pythonClustering.JPG",
      summary:
        "Python program which performs Ripley's K/L analysis, DBSCAN clustering, and OPTICS clustering",
      preview: "https://github.com/jesse-anderson/Python/tree/main/Cluster-Analysis-with-GUI",
      techStack: ["Python","Cluster Analysis"],
    },
  ],

  researchProjects: [
    {
      projectName: "Increased vesicular dynamics and nanoscale clustering of IL-2 after T cell activation",
      image: "images/VesiclesPaper.png",
      summary:
        "In this study, DBSCAN clustering analyzed IL-2 distribution in Jurkat T cells via dSTORM imaging, revealing that T cell activation results in more pronounced and elongated nanoscale clusters compared to controls.",
      preview: "https://www.sciencedirect.com/science/article/abs/pii/S0006349524002091",
      techStack: ["Immunology","MATLAB", "Cluster Analysis", "DBSCAN"],
    },
    {
      projectName: "Superresolution Imaging with Single-Antibody Labeling",
      image: "images/DBSCANresearch.JPG",
      summary:
        "The project uses DBSCAN clustering as a means of identifying high density regions in superresolution imaging with single-antibody labeling.",
      preview: "https://pubs.acs.org/doi/full/10.1021/acs.bioconjchem.3c00178",
      techStack: ["MATLAB", "Cluster Analysis", "DBSCAN"],
    },
  ],
  cheProjects: [
    {
      projectName: "Smog Modeling as Chemical Engineering",
      image: "images/smogModel.jpg",
      summary:
        "A model of accumulation and depletion of smog in Los Angeles was modeled in MATLAB.",
      preview: "https://github.com/jesse-anderson/MATLAB/tree/main/Chemical_Engineering/Modeling-Smog-In-LA",
      techStack: ["MATLAB","Chemical Engineering"],
    },
    {
      projectName: "Biochemical Plant Simulation",
      image: "images/seniorDesign.jpg",
      summary:
        "Simulated a l. reuteri 1,3-propanediol plant producing ~60,000 tons/year. Project won 1st Place in the Engineering Expo at UIC 2023, ChE Division. ",
        
      preview: "files/seniorDesign.pdf",
      techStack: ["Aspen Plus","SuperPro Designer", "Chemical Engineering"],
    },
  ],
  webProjects: [
    {
      projectName: "Oak Park Crime Reporting",
      image: "images/OP-Crime.jpg",
      summary:
        "Developed an ETL pipeline to parse Oak Park crimes and place into a Folium static web application to track crimes over time. Updated daily using a raspberry pi, pushed to a weekly mailing list, and NLP enabled to determine commonalities across incidents.",
      preview: "https://jesse-anderson.net/OP-Crime-Maps/map",
      techStack: ["Python", "ETL", "AWS", "GCP", "NLP"],
    },
    {
      projectName: "UIC Faculty Web Scraping",
      image: "images/webScraping.png",
      summary:
        "Developed an automated python script to scrape from the web University of Illinois Faculty Information via Beautiful Soup and shown via a Flask implementation to display data on a local server.",
      preview: "https://github.com/jesse-anderson/Python/tree/main/Python-Flask-Web-Scraping",
      techStack: ["Python","Beautiful Soup", "Flask"],
    },
    {
      projectName: "Pyodide Project Online Python Execution",
      image: "images/pyodide-logo.png",
      summary:
        "Pyodide project to showcase spherical Random Number Generation and perform OPTICS clustering on the spheres. Proof of concept Python in browser via Pyodide.",
      preview: "https://jesse-anderson.github.io/files/pyodide_runCalcs.html",
      techStack: ["Python", "Pyodide", "Clustering"],
    },
  ],
};

export const experience = [
  {
    title: "Engineer",
    duration: "June 2023 - April 2024",
    subtitle: "UL Solutions",
    details: [
    "Develop automation software in Python and VBA to eliminate 533+ hours of tedious workflows annually.",
    "Develop software to automatically detect changes in CAD files and alert engineers to such changes in Python using OpenCV/PyMuPDF.",
    "Enhance data driven decision making by implementing real time data analysis for Large Scale testing.",
    ],
    tags: ["Engineering", "Python", "VBA", "CAD", "Fire Protection"],
    icon: "gears",
  },
  {
    title: "Undergraduate Research",
    duration: "December 2020 - June 2023",
    subtitle: "University of Illinois at Chicago",
    details: [
      "Developed novel software in MATLAB, R, and Python for image and computational analysis of single molecule localization microscopy images.",
      "Utilized clustering algorithms (DBSCAN/OPTICS/Ripley's K) to determine spatiotemporal properties of single-molecule localizations.",
      "Optimized existing numerical algorithms to decrease the time it takes for a bottlenecked lab operation by 267%."
    ],
    tags: ["MATLAB", "R", "C++","Python"],
    icon: "flask",
  },
  {
    title: "Engineering Intern",
    duration: "May 2022 - August 2022",
    subtitle: "United Conveyor Corporation",
    details: [
      "Develop engineering software in VBA to automate design workflow and assist in engineering design calculations.",
    "Developed software to improve analysis workflow bottleneck by 540,000% by eliminating manual data entry.",
    "Automated 150 hours/yr of data entry, comparison and analysis tasks.",
    "Created and implemented a library of software tools for thermoplastic and thermoset material property analysis per ASME/AWWA/PPI standards."

    ],
    tags: ["VBA-Excel", "P&ID"],
    icon: "gears",
  },
  {
    title: "Peer Leader, Calculus Based Physics",
    duration: "August 2020 - December 2021",
    subtitle: "Conveyor & Piping Support Design",
    details: [
      "Ensured student success in Calculus-Based Physics (Mechanics) via one-on-one and group tutoring through online platforms (Blackboard, Zoom) with a focus on problem solving methodology.",
    "Developed an automated attendance analytics program to measure student attrition in Physics I."
    ],
    tags: ["VBA-Excel"],
    icon: "gears",
  },
  {
    title: "Safety/Project Manager",
    duration: "June 2016-August 2019",
    subtitle: "G5 Environmental",
    details: [
      "Served as project lead at job sites by ensuring  completion of contract requirements by CDL team members",
    "Ensured safe execution of any mechanical repairs by mechanics.",
    "Acquired parts on an as needed basis to ensure that contracts serviced did not experience time offline"
    ],
    tags: ["VBA-Excel"],
    icon: "gears",
  },
];

export const education = [
  {
    title: "Master's in Computer Science",
    duration: "",
    subtitle: "University of Illinois at Urbana-Champaign",
    details: [
      "IN PROGRESS",
      "GPA: 4.00",
      "Courses Completed: Applied Machine Learning, Practical Statistical Learning, Distributed Systems, Methods of Applied Statistics",
      "Professional Master of Computer Science (MCS) at UIUC. The University of Illinois CS graduate program is ranked 5th by U.S. News & World Report (2022)."
    ],
    tags: [
      "Machine Learning",
      "AI",
      "Python",
      "Automation",
    ],
    icon: "graduation-cap",
  },
  {
    title: "Bachelors in Chemical Engineering",
    duration: "",
    subtitle: "University of Illinois at Chicago",
    details: [
      "I completed my degree with a final GPA of 3.77 and concentrations in Biochemical Engineering and Process Automation.",
      "My minor was in Mathematics & Computer Science where I completed 2 courses in Python, Discrete Math, Data Structures in C++, and Industrial Mathematics[400 level].",
      "My education exposed me to Computer Science as a tool to solve difficult problems and I keep that mentality as I learn new skillsets.",
    ],
    tags: [
      "Data Structures & Algorithms",
      "Python",
      "ASPEN Plus",
      "SuperPro Designer",
      "SnapGene",
      "Raspberyy Pi",
    ],
    icon: "graduation-cap",
  },
  {
    title: "Associate's In Science",
    duration: "",
    subtitle: "College of DuPage",
    details: [
      "Completion of A.S. with coursework in Chemistry, Biology, and Mathematics with a final GPA of 3.65",
      "Additionally, I am proud to have presented at the college's research symposium where I presented on the topic of Learned Helplessness",
      
    ],
    tags: ["Chemistry", "Biology", "Mathematics"],
    icon: "book",
  },
];
export const volunteering = [
  {
    title: "Remote Area Medical",
    duration: "July 2018-August 2018",
    subtitle: "Equipment Technician",
    details: [
      "Volunteer to assist medical providers in providing care in remote areas to underserved populations.",
      "Maintain generators, hydraulic/pneumatic dental tools, mix sanitizing agents on site, and worksite preparations.",
      "Disposal of hazardous waste post treatment.",
    ],
    tags: [""],
    icon: "heart",
  },
];


export const footer = [
  {
    label: "Dev Profiles",
    data: [
      {
        text: "GitHub",
        link: "https://github.com/jesse-anderson",
      },
      {
        text: "Kaggle",
        link: "https://www.kaggle.com/jesseanderson777",
      },
      {
        text: "LeetCode",
        link: "https://leetcode.com/Jesse-Anderson/",
      },
    ],
  },
  {
    label: "Resources",
    data: [
      {
        text: "Enable Dark/Light Mode",
        func: "enableDarkMode()",
      },
      {
        text: "Print this page",
        func: "window.print()",
      },
      {
        text: "Clone this page",
        link: "https://github.com/jesse-anderson/jesse-anderson.github.io",
      },
    ],
  },
  {
    label: "Social Profiles",
    data: [
      {
        text: "Linkedin",
        link: "https://www.linkedin.com/in/jesse-anderson-a7c5/",
      },
      {
        text: "ORCID",
        link: "https://orcid.org/0000-0001-5731-5511",
      },
      {
        text: "Buy me a coffee",
        link: "https://www.buymeacoffee.com/JesseAnderson",
      },
    ],
  },
  {
    label: "copyright-text",
    data: [
      "Made with &hearts; by Jesse Anderson.",
      "&copy; No Copyrights. Feel free to use this template.",
    ],
  },
];

const gitUserName = "jesse-anderson";
const mediumUserName = "Jesse-Anderson";

export const URLs = {
  mediumURL: `https://api.rss2json.com/v1/api.json?rss_url=https://medium.com/feed/@${mediumUserName}`,
  quartoURL: 'https://blog.jesse-anderson.net/'
};
