function populateSkills(skills)
{
    console.log(skills)
    const skillsContainer = document.getElementById("skillsContainer");
    skills.forEach(element => {
        const skill = document.createElement("li");
        skill.textContent = element;
        skillsContainer.appendChild(skill);
    });
}
