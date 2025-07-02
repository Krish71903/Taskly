import React from 'react';

const Login: React.FC = () => {
  const handleLogin = () => {
    // Redirect to the backend's Google login URL
    window.location.href = 'http://localhost:8000/auth/login';
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gray-100">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-8">Taskly</h1>
        <button
          onClick={handleLogin}
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          Login with Google
        </button>
      </div>
    </div>
  );
};

export default Login; 