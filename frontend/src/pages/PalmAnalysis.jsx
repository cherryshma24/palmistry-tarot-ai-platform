import { useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  FaHome,
  FaHandSparkles,
  FaStar,
  FaChartLine,
  FaUserCircle,
  FaSignOutAlt,
  FaCloudUploadAlt
} from "react-icons/fa";

import api from "../services/api";
import "./PalmAnalysis.css";


function PalmAnalysis() {


const navigate = useNavigate();


const [image,setImage]=useState(null);

const [preview,setPreview]=useState(null);

const [loading,setLoading]=useState(false);






const handleImage=(e)=>{


const file=e.target.files[0];


if(!file) return;


setImage(file);


setPreview(
URL.createObjectURL(file)
);


};








const analyzePalm=async()=>{


if(!image){

alert("Please upload your palm image.");

return;

}



const token=localStorage.getItem("access_token");



const formData=new FormData();


formData.append(
"file",
image
);



try{


setLoading(true);



const response=await api.post(

"/palm/analyze",

formData,

{

headers:{

Authorization:`Bearer ${token}`,

"Content-Type":"multipart/form-data",

}

}

);





localStorage.setItem(

"analysis_result",

JSON.stringify(response.data)

);



navigate("/report");




}

catch(error){


console.log(error);

alert("Palm analysis failed.");


}

finally{


setLoading(false);


}



};







return (



<div className="analysis-layout">





{/* SIDEBAR */}


<aside className="sidebar">


<div className="logo">

🔮 PalmAI

</div>



<div className="menu">


<div 
className="menu-item"
onClick={()=>navigate("/dashboard")}
>

<FaHome/>

Dashboard

</div>



<div className="menu-item active">

<FaHandSparkles/>

Palm Analysis

</div>



<div className="menu-item">

<FaStar/>

Tarot Reading

</div>



<div className="menu-item">

<FaChartLine/>

Reports

</div>



<div className="menu-item">

<FaUserCircle/>

Profile

</div>



</div>



<div 
className="logout"
onClick={()=>{

localStorage.removeItem("access_token");

navigate("/");

}}
>

<FaSignOutAlt/>

Logout

</div>


</aside>









{/* MAIN */}



<main className="analysis-main">





<div className="analysis-header">


<h1>

🤖 AI Palm Analysis

</h1>



<p>

Upload your palm image and let AI detect hand landmarks,
extract features and generate your personalized reading.

</p>


</div>







<div className="upload-card">





<div className="ai-badge">

✨ Artificial Intelligence Vision

</div>






<h2>

Upload Your Palm Image

</h2>





<p>

Upload a clear image of your dominant palm.
AI will detect 21 hand landmarks and analyze palm features.

</p>







<label className="upload-area">


<input

type="file"

accept="image/*"

hidden

onChange={handleImage}

/>





{

preview ? (



<div className="preview-box">


<img

src={preview}

alt="Palm Preview"

/>


<h3>

{image.name}

</h3>


<span>

{(image.size/1024/1024).toFixed(2)} MB

</span>



</div>



):(



<>


<FaCloudUploadAlt className="upload-icon"/>


<h3>

Click to Upload Palm Image

</h3>


<p>

JPG / PNG / JPEG

<br/>

High resolution image recommended

</p>



</>


)

}



</label>







<button

className="analyze-btn"

onClick={analyzePalm}

disabled={loading}

>


{

loading

?

"🔄 AI Analyzing..."

:

"✨ Start AI Analysis"

}



</button>






</div>







</main>




</div>



);


}


export default PalmAnalysis;