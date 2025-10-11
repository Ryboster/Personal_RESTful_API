// Receive the list of skills from the backend and while 
// containerizing each skill, populate the "skills" list in the template. 
function populateSkills(skills)
{
    console.log(skills)
    const skillsContainer = document.getElementById("skillsList");
    skills.forEach(element => {
        const skill = document.createElement("li");
        skill.textContent = element;
        skillsContainer.appendChild(skill);
    });
}