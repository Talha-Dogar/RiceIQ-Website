import HeroSection from "./heroSection";
import Navbar from "./navbar";
import ProductFeatureSection from "./productFeature";
import HowItWorks from "./howitworks";
import WhyChooseUs from "./whyChooseUs";
import Contact from "./contact";
import Footer from "../../components/footer/Footer";
const Home = () => {
  return (
    <div>
      <Navbar />
      <HeroSection />
      <ProductFeatureSection />
      <HowItWorks />
      {/* <LandscapeImage/> */}
      <WhyChooseUs />
      <Contact/>
      <Footer />
    </div>
  );
};
export default Home;
