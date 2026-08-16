import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Profile from "./pages/Profile";
import Analysis from "./pages/Analysis";
import Report from "./pages/Report";
import PalmAnalysis from "./pages/PalmAnalysis";

import Tarot from "./pages/Tarot";
import TarotReport from "./pages/TarotReport";
import TarotResult from "./pages/TarotResult";

import ProtectedRoute from "./components/ProtectedRoute";


function App() {

  return (

    <BrowserRouter>

      <Routes>


        {/* =====================
            Public Routes
        ====================== */}

        <Route
          path="/"
          element={<Login />}
        />


        <Route
          path="/register"
          element={<Register />}
        />



        {/* =====================
            Dashboard
        ====================== */}

        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />



        {/* =====================
            User Profile
        ====================== */}

        <Route
          path="/profile"
          element={
            <ProtectedRoute>
              <Profile />
            </ProtectedRoute>
          }
        />



        {/* =====================
            Palm Analysis Upload
        ====================== */}

        <Route
          path="/palm-upload"
          element={
            <ProtectedRoute>
              <PalmAnalysis />
            </ProtectedRoute>
          }
        />



        {/* =====================
            AI Palm Analysis Loading
        ====================== */}

        <Route
          path="/analysis"
          element={
            <ProtectedRoute>
              <Analysis />
            </ProtectedRoute>
          }
        />



        {/* =====================
            Palm Analysis Report
        ====================== */}

        <Route
          path="/report"
          element={
            <ProtectedRoute>
              <Report />
            </ProtectedRoute>
          }
        />



        {/* =====================
            Tarot Reading
        ====================== */}

        <Route
          path="/tarot"
          element={
            <ProtectedRoute>
              <Tarot />
            </ProtectedRoute>
          }
        />











       
      {/* =====================
            Tarot Result
        ====================== */}


        <Route
         path="/tarot-result"
         element={
         <ProtectedRoute>
         <TarotResult />
         </ProtectedRoute>
         }
      />



        {/* =====================
            Tarot Report
        ====================== */}

        <Route
          path="/tarot-report"
          element={
            <ProtectedRoute>
              <TarotReport />
            </ProtectedRoute>
          }
        />



      </Routes>



 


    </BrowserRouter>

  );

}


export default App;