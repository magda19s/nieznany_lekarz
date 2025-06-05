import { Navigate, Outlet } from "react-router-dom";
import { useAtom } from "jotai";
import { roleState } from "@/state/role";

type PrivateRouteProps = {
  allowedRoles: string[];
};

export default function PrivateRoute({ allowedRoles }: PrivateRouteProps) {
  const [role] = useAtom(roleState);

  if (!role || !allowedRoles.includes(role)) {
    return <Navigate to="/" replace />;
  }

  return <Outlet />;
}
