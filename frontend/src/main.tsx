import './index.css'
import App from '@/App.tsx'
import HomePage from '@/pages/Home.tsx'
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import ReactDOM from "react-dom/client";
import React from "react";
import { GoogleOAuthProvider } from '@react-oauth/google';

const router = createBrowserRouter([
  {
    path: "",
    element: <App />,
    children: [
      {
        path: "",
        element: <HomePage />,
      },
      {
        path: "*",
        element: <>Not Found</>,
      },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <GoogleOAuthProvider clientId="526474343190-8vun9une71fnhb689k4rjoootlmbgo00.apps.googleusercontent.com">
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
  </GoogleOAuthProvider>,
);
