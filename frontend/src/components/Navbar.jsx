import { Link, useNavigate } from "react-router-dom";
import {
  FaHandSparkles,
  FaHome,
  FaUserCircle,
  FaSignOutAlt,
  FaBell
} from "react-icons/fa";

import "./Navbar.css";

function Navbar() {

  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    navigate("/");
  };

  return (

<nav className="navbar">


<div className="logo">


<FaHandSparkles className="logo-icon"/>


<div>

<h2>
Palmistry AI
</h2>


<span>
Intelligence Platform
</span>


</div>


</div>





<div className="nav-links">


<Link to="/dashboard">

<FaHome/>

Dashboard

</Link>



<Link to="/profile">

<FaUserCircle/>

Profile

</Link>


</div>






<div className="nav-right">


<div className="notification">


<FaBell/>

<span className="dot"></span>


</div>





<button

className="logout-btn"

onClick={handleLogout}

>


<FaSignOutAlt/>

Logout


</button>




</div>



</nav>

);

}

export default Navbar;