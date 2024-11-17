import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./Components/Home";
import SignUp from "./Components/SignUp";
import SignIn from "./Components/SignIn";
import MainDisplay from "./Components/MainDispaly";
import SendGrid from "./Components/SendGrid";
import Gmail from "./Components/Gmail";
import SendGridApi from "./Components/SendGridApi";

function App() {
  return (
    <Router>
      <Routes>
        <Route path='/' element={<Home/>} />
        <Route path="/signup" element={<SignUp />} /> 
        <Route path="/signin" element={<SignIn/>} />
        <Route path="/main-display" element={<MainDisplay />} />
        <Route path="/sendgrid" element={<SendGrid/>}/>
        <Route path="/sendgrid-api" element={<SendGridApi/>}/>
        <Route path="/gmail" element={<Gmail/>}/>
      </Routes>
    </Router>
  );
}

export default App;