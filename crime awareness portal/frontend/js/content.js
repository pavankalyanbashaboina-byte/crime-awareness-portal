// Crime data
const crimeData = {
    // Student Crimes
    ragging: {
        name: "Ragging (Bullying of Juniors)",
        description: "Ragging is one of the most serious offenses in colleges, where senior students mentally or physically harass juniors to assert dominance or for entertainment. It may include verbal abuse, forcing students to perform humiliating acts, physical assault, or psychological pressure. Ragging creates fear, trauma, and sometimes leads to severe mental health issues or even suicides. To prevent this, strict regulations are enforced by educational authorities, and institutions maintain anti-ragging committees to monitor and act on complaints immediately.",
        legal: "UGC Anti-Ragging Regulations",
        punishment: "Suspension, expulsion, imprisonment up to 2–3 years",
        fine: "₹25,000 to ₹1,00,000; treated as a criminal offense with FIR registration"
    },
    drug: {
        name: "Drug Use or Drug Distribution",
        description: "Drug abuse in colleges involves students consuming or distributing narcotic substances within campus or hostels. This not only harms the individual's health but also disrupts the academic environment and may lead to addiction, violence, or illegal activities. Drug distribution is considered a severe crime as it contributes to the spread of substance abuse among youth and attracts strict legal consequences.",
        legal: "Narcotic Drugs and Psychotropic Substances Act",
        punishment: "6 months to 20 years imprisonment",
        fine: "₹10,000 to ₹2,00,000+; non-bailable offense in serious cases"
    },
    violence: {
        name: "Physical Violence / Fighting",
        description: "Physical violence in colleges includes fights, assaults, or attacks between students due to personal conflicts, group rivalries, or political issues. Such behavior disrupts campus peace and may cause serious injuries or long-term consequences for victims. Violence is strictly prohibited, and colleges take strict disciplinary actions along with legal proceedings.",
        legal: "Indian Penal Code Section 351",
        punishment: "Imprisonment up to 1–7 years",
        fine: "₹1,000 to ₹50,000; punishable depending on severity"
    },
    cyberbullying: {
        name: "Cyberbullying and Online Harassment",
        description: "Cyberbullying involves using digital platforms to threaten, defame, or harass others. This includes creating fake profiles, spreading rumors, posting private content without consent, or sending abusive messages. With the increasing use of social media, such crimes are rising and can severely impact a victim's mental health and reputation.",
        legal: "Information Technology Act, 2000",
        punishment: "Imprisonment up to 3 years",
        fine: "Fine up to ₹5,00,000"
    },
    cheating: {
        name: "Cheating in Exams",
        description: "Cheating in exams includes copying answers, using unauthorized devices, or impersonation. It affects the fairness of the academic system and undermines merit-based evaluation. Though mostly handled at the institutional level, serious cases like impersonation may lead to legal action.",
        legal: "Institutional rules / fraud-related laws",
        punishment: "Exam cancellation, debarment for 1–3 years",
        fine: "Academic penalty; legal action if fraud involved"
    },
    theft: {
        name: "Theft",
        description: "Theft in colleges refers to stealing personal belongings like mobiles, laptops, or institutional property. It creates insecurity among students and disrupts trust within the campus environment.",
        legal: "Indian Penal Code Section 379",
        punishment: "Imprisonment up to 3 years",
        fine: "Monetary fine imposed by court"
    },
    harassment: {
        name: "Sexual Harassment",
        description: "Sexual harassment includes unwanted physical contact, inappropriate messages, or verbal abuse of a sexual nature. It is a serious violation of dignity and safety, and strict actions are taken by both colleges and law enforcement agencies.",
        legal: "Sexual Harassment of Women at Workplace Act",
        punishment: "Imprisonment up to 3 years",
        fine: "Compensation + legal penalty"
    },
    vandalism: {
        name: "Property Damage / Vandalism",
        description: "Vandalism involves damaging college property such as classrooms, labs, or hostels, often during protests or conflicts. It leads to financial loss and disruption of academic activities.",
        legal: "Prevention of Damage to Public Property Act",
        punishment: "Imprisonment up to 5 years",
        fine: "Payment of damages + penalty"
    },
    // Faculty Crimes
    sexualHarassmentFaculty: {
        name: "Sexual Harassment by Faculty",
        description: "When faculty misuse their authority to harass students, it creates an unsafe and exploitative environment. Such actions damage trust and violate professional ethics and legal standards.",
        legal: "Sexual Harassment of Women at Workplace Act",
        punishment: "3–7 years imprisonment + job termination",
        fine: "Compensation + legal action"
    },
    bribery: {
        name: "Bribery / Corruption",
        description: "Corruption in colleges involves faculty demanding money or favors in exchange for marks or attendance. This undermines fairness and damages the integrity of the education system.",
        legal: "Prevention of Corruption Act",
        punishment: "3–7 years imprisonment",
        fine: "Monetary fine + dismissal"
    },
    fraud: {
        name: "Academic Fraud / Plagiarism",
        description: "Faculty committing plagiarism or falsifying research harms academic credibility and violates research ethics.",
        legal: "Institutional + copyright laws",
        punishment: "Job termination",
        fine: "Academic penalties"
    },
    discrimination: {
        name: "Discrimination",
        description: "Discrimination based on caste, religion, or gender affects equality and student rights.",
        legal: "SC/ST Prevention of Atrocities Act",
        punishment: "Imprisonment up to 5 years",
        fine: "Compensation to victim"
    },
    authority: {
        name: "Misuse of Authority",
        description: "Faculty may exploit students by forcing personal work or threatening academic performance.",
        legal: "Institutional rules",
        punishment: "Suspension or dismissal",
        fine: "Institutional penalties"
    },
    leakage: {
        name: "Exam Paper Leakage",
        description: "Leaking exam papers before exams is a serious crime affecting the integrity of education.",
        legal: "Criminal breach of trust laws",
        punishment: "3–10 years imprisonment",
        fine: "Heavy penalty + dismissal"
    },
    // Shared Crimes
    cybercrime: {
        name: "Cybercrime",
        description: "Cybercrime includes hacking, data theft, and online fraud affecting individuals or institutions.",
        legal: "Information Technology Act, 2000",
        punishment: "3–5 years imprisonment",
        fine: "Up to ₹5,00,000"
    },
    defamation: {
        name: "Defamation",
        description: "Defamation involves spreading false information that harms someone's reputation.",
        legal: "Indian Penal Code Section 499",
        punishment: "Up to 2 years imprisonment",
        fine: "Monetary fine"
    },
    forgery: {
        name: "Forgery of Documents",
        description: "Forgery of documents refers to creating fake certificates, marksheets, identity cards, or altering official academic records to gain unfair advantage such as admission, job opportunities, or exam eligibility. In colleges, this may include fake attendance records, manipulated grades, or counterfeit internship certificates. Such actions not only damage institutional credibility but also violate trust and legal standards. Forgery is treated as a serious criminal offense because it involves intentional deception and misuse of official documentation.",
        legal: "Indian Penal Code Section 465, Indian Penal Code Section 468",
        punishment: "Imprisonment up to 2–7 years depending on severity",
        fine: "Monetary fine imposed by court; punishable as a criminal offense involving fraud"
    },
    identity: {
        name: "Identity Theft",
        description: "Identity theft occurs when a person uses another individual's personal information such as Aadhaar details, login credentials, student ID, or banking information without permission for fraudulent purposes. In college settings, this may involve impersonating someone in exams, accessing accounts, or committing financial fraud using stolen identities. With increasing reliance on digital platforms, identity theft has become a major concern and is strictly punishable under cyber laws in India.",
        legal: "Information Technology Act Section 66C",
        punishment: "Imprisonment up to 3 years",
        fine: "Fine up to ₹1,00,000; treated as a cybercrime offense"
    },
    financial: {
        name: "Financial Fraud",
        description: "Financial fraud in a college environment involves illegal activities such as cheating others for money, creating fake payment links, manipulating fees, scholarship scams, or unauthorized transactions using digital platforms. Students or faculty may misuse online payment systems, banking details, or institutional funds for personal gain. With the rise of digital transactions, such frauds have increased and can cause serious financial loss to individuals and institutions. These acts are considered serious economic offenses and are punishable under multiple provisions of criminal and cyber laws in India.",
        legal: "Indian Penal Code Section 420, Information Technology Act, 2000",
        punishment: "Imprisonment up to 7 years (can extend in severe cases)",
        fine: "Heavy monetary fine; considered a non-bailable offense in major fraud cases"
    }
};

// Color mapping
const colorMap = {
    purple: "#800080",
    pink: "#FFC0CB",
    orange: "#FF8C00",
    magenta: "#FF00FF",
    green: "#008000"
};

// Function to show crime details
function showCrime(crimeKey, buttonClass) {
    const box = document.getElementById("contentBox");
    const crime = crimeData[crimeKey];

    if (!crime) {
        box.innerHTML = "<p>Crime information not found.</p>";
        box.classList.add("show");
        return;
    }

    box.innerHTML = `
        <button class="close-btn" onclick="closeModal()">&times;</button>
        <h3>${crime.name}</h3>
        <p>${crime.description}</p>
        <p><strong>Applicable Legal Sections:</strong> ${crime.legal}</p>
        <p><strong>Punishment Details:</strong> ${crime.punishment}</p>
        <p><strong>Fine & Punishable Offence:</strong> ${crime.fine}</p>
    `;

    // Set border color and glow effect
    const borderColor = colorMap[buttonClass] || "#000080";
    box.style.borderColor = borderColor;
    box.style.boxShadow = `0 0 30px ${borderColor}60, 0 8px 24px rgba(0, 0, 0, 0.3)`;

    box.classList.add("show");
}

// Function to close modal
function closeModal() {
    const box = document.getElementById("contentBox");
    box.classList.remove("show");
}

// Event listener for crime buttons
document.addEventListener("DOMContentLoaded", function() {
    const buttons = document.querySelectorAll(".crime-btn");
    buttons.forEach(button => {
        button.addEventListener("click", function() {
            const crimeKey = this.getAttribute("data-crime");
            const buttonClass = Array.from(this.classList).find(cls => colorMap[cls]);
            showCrime(crimeKey, buttonClass);
        });
    });

    // Close modal when clicking outside
    document.addEventListener("click", function(event) {
        const box = document.getElementById("contentBox");
        if (event.target === box) {
            closeModal();
        }
    });

    // Close modal on Escape key
    document.addEventListener("keydown", function(event) {
        if (event.key === "Escape") {
            closeModal();
        }
    });
});