export const scrollToHome = () =>{
    const Home = document.getElementById("home");
    if (Home)
        {
            Home.scrollIntoView({behavior:"smooth"});
        }
    
    }