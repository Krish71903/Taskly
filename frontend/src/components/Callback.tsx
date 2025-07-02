import React, { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

const Callback: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();

  useEffect(() => {
    const searchParams = new URLSearchParams(location.search);
    const code = searchParams.get('code');

    if (code) {
      // Send the code to the backend to exchange for a token
      // fetch(`http://localhost:8000/auth/callback?code=${code}`)
      //   .then(response => response.json())
      //   .then(data => {
      //     // Store the token (e.g., in localStorage)
      //     localStorage.setItem('authToken', data.access_token);
      //     // Redirect to the dashboard
      //     navigate('/dashboard');
      //   });
      console.log("Received auth code:", code);
      // For now, just redirect to dashboard
      navigate('/dashboard');

    } else {
      // Handle error or redirect to login
      navigate('/login');
    }
  }, [location, navigate]);

  return <div>Loading...</div>;
};

export default Callback; 