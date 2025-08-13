export const scrollToContact = () =>{
    const Contact = document.getElementById("contact");
    if (Contact)
        {
            Contact.scrollIntoView({behavior:"smooth"});
        }
    
    }