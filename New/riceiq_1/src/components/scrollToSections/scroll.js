export const scrollToFeatures = () =>{
    const Features = document.getElementById("features");
    if (Features)
        {
            Features.scrollIntoView({behavior:"smooth"});
        }
    
    }