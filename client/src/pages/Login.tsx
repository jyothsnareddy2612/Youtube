import { GoogleLogin } from "@react-oauth/google";
import axios from "axios";
import { useState } from "react";
import { useAuthStore } from "../store/useAuthStore";

const Login = () => {
  const { user, setAuth, logout } = useAuthStore();
  const [file, setFile] = useState<File | null>(null);

  const handleSuccess = async (res: any) => {
    try {
      const response = await axios.post("http://localhost:8000/oauth/google", {
        token: res.credential,
      });

      setAuth(response.data.user, response.data.access_token);
    } catch (error) {
      console.error(error);
    }
  };

  const uploadProfile = async () => {
    if (!file || !user) return;

    const formData = new FormData();
    formData.append("file", file);
    formData.append("email", user.email);

    await axios.post("http://localhost:8000/user/upload-profile", formData);

    window.location.reload(); // simple refresh
  };

  return (
    <div className="h-screen flex items-center justify-center bg-gray-900">
      
      {!user && (
        <GoogleLogin
          onSuccess={handleSuccess}
          onError={() => console.log("Login Failed")}
        />
      )}

      {user && (
        <div className="text-white text-center">
          <img
            src={user.picture}
            alt="profile"
            className="w-20 h-20 rounded-full mx-auto mb-4"
          />

          <h2>{user.name}</h2>
          <p>{user.email}</p>

          <input
            type="file"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
          />

          <button
            onClick={uploadProfile}
            className="bg-blue-500 px-4 py-2 mt-2 rounded"
          >
            Upload Profile
          </button>

          <button
            onClick={logout}
            className="bg-red-500 px-4 py-2 mt-4 rounded"
          >
            Logout
          </button>
        </div>
      )}
    </div>
  );
};

export default Login;