import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import {
  FaUser,
  FaBirthdayCake,
  FaMagic,
  FaClipboardList,
  FaUserCircle
} from "react-icons/fa";


import api from "../services/api";
import "./Dashboard.css";


function Dashboard() {


  const navigate = useNavigate();


  const [user, setUser] = useState(null);



  const [formData, setFormData] = useState({

    age: "",
    gender: "",
    dob: "",
    birthTime: "",
    birthPlace: "",
    dominantHand: "",
    relationship: "",
    occupation: "",
    interest: "",
    notes: "",

  });





  useEffect(() => {


    const fetchProfile = async () => {


      const token = localStorage.getItem("access_token");


      if (!token) {

        navigate("/");

        return;

      }



      try {


        const response = await api.get(
          "/auth/profile",
          {

            headers: {

              Authorization: `Bearer ${token}`,

            },

          }
        );


        setUser(response.data);



      } catch(error) {


        console.log(error);

        localStorage.removeItem("access_token");

        navigate("/");


      }


    };



    fetchProfile();



  }, [navigate]);







  const handleChange = (e)=>{


    setFormData({

      ...formData,

      [e.target.name]:e.target.value

    });


  };







  const handleSubmit=(e)=>{


    e.preventDefault();



    const profileData={

      ...user,

      ...formData

    };



    localStorage.setItem(

      "user_profile",

      JSON.stringify(profileData)

    );



    navigate("/palm-upload");


  };







  return (


<div className="dashboard-layout">

    <Sidebar />

    <main className="dashboard-main">

        {/* Your dashboard content */}

    <header className="dashboard-header">


   <div>


     <h1>

        Welcome back, {user?.full_name || "User"} 👋

    </h1>


    <p>

        Complete your profile to begin your personalized AI Palm & Tarot Reading.

    </p>


  </div>



<div className="profile-badge">

<FaUserCircle/>

</div>



</header>







<form onSubmit={handleSubmit}>


<div className="dashboard-grid">







<div className="glass-card">


<h2>

<FaUser/>

Personal Information

</h2>




<label>
Full Name
</label>


<input

value={user?.full_name || ""}

readOnly

/>




<label>
Email
</label>


<input

value={user?.email || ""}

readOnly

/>



<label>Age</label>
<input
  type="number"
  name="age"
  value={formData.age}
  onChange={handleChange}
  required
/>

<label>Gender</label>
<select
  name="gender"
  value={formData.gender}
  onChange={handleChange}
  required
>
  <option value="">Select Gender</option>
  <option value="Male">Male</option>
  <option value="Female">Female</option>
  <option value="Other">Other</option>
</select>





</div>









<div className="glass-card">


<h2>

<FaBirthdayCake/>

Birth Details

</h2>




<label>
Date of Birth
</label>


<input

type="date"

name="dob"

value={formData.dob}

onChange={handleChange}

/>





<label>
Birth Time
</label>


<input

type="time"

name="birthTime"

value={formData.birthTime}

onChange={handleChange}

/>






<label>
Birth Place
</label>


<input

name="birthPlace"

value={formData.birthPlace}

onChange={handleChange}

/>



</div>









<div className="glass-card">


<h2>

<FaMagic/>

Reading Preferences

</h2>



<label>
Interest

</label>


<select

name="interest"

value={formData.interest}

onChange={handleChange}

>


<option>

Select

</option>


<option>

Love

</option>


<option>

  Health 

</option>

<option>

Career

</option>


<option>

Finance

</option>


<option>

Education

</option>



</select>






<label>
Occupation

</label>


<input

name="occupation"

value={formData.occupation}

onChange={handleChange}

/>



</div>









<div className="glass-card">


<h2>

<FaClipboardList/>

Additional Notes

</h2>




<textarea

rows="5"

name="notes"

value={formData.notes}

onChange={handleChange}

placeholder="Anything you'd like AI to know..."

></textarea>



</div>






</div>






<div className="feature-row">



<div
  className="feature-card"
  onClick={() => navigate("/palm-upload")}
>

🔮

<h3>

Palm Analysis

</h3>


<p>

AI based palm feature extraction

</p>


</div>






<div
  className="feature-card"
  onClick={() => navigate("/tarot")}
>

⭐

<h3>

Tarot Intelligence

</h3>


<p>

Personalized tarot interpretation

</p>


</div>






<div
  className="feature-card"
  onClick={() => navigate("/history")}
>

📊

<h3>

AI Reports

</h3>


<p>

Generated reading reports

</p>


</div>



</div>







<button

type="submit"

className="continue-btn"

>


Continue to Palm Analysis →

</button>






</form>




</main>




</div>



  );

}


export default Dashboard;