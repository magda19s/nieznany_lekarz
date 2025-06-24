import './index.css'
import App from '@/App.tsx'
import HomePage from '@/pages/Home.tsx'
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import ReactDOM from "react-dom/client";
import React from "react";
import { GoogleOAuthProvider } from '@react-oauth/google';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import BookAService from '@/pages/BookService';
import AboutUs from '@/pages/AboutUs';
import Contact from '@/pages/Contact';
import PrivateRoute from './PrivateRoute';
import Payment from './pages/Payment';
import PaymentStatus from './pages/PaymentStatus';
import Visits from './pages/Visits';

const queryClient = new QueryClient();

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
        path: "/payment/redirect",
        element: <PaymentStatus />,
      },
      {
        element: <PrivateRoute allowedRoles={["patient"]} />,
        children: [
          {
            path: "/new-service",
            element: <BookAService />,
          },
          {
            path: "/payment",
            element: <Payment />,
          },
        ],
      },
      {
        element: <PrivateRoute allowedRoles={["patient", "doctor"]} />,
        children: [
          {
            path: "/my-services",
            element: <Visits />,
          },
        ],
      },
      {
        path: "/about-us",
        element: <AboutUs />,
      },
      {
        path: "/contact",
        element: <Contact />,
      },
      {
        path: "*",
        element: <>Not Found</>,
      },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <GoogleOAuthProvider clientId={import.meta.env.VITE_AUTH_CLIENT_ID}>
        <RouterProvider router={router} />
      </GoogleOAuthProvider>
    </QueryClientProvider>
  </React.StrictMode>
);
