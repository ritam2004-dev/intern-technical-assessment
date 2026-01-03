import { useEffect } from "react";
import AppRoutes from "./routes/AppRoutes";
import { useAuthStore } from "./store/authStore";
import Loader from "./components/ui/Loader";

export default function App() {
  const checkAuth = useAuthStore((s) => s.checkAuth);
  const { isCheckingAuth } = useAuthStore();

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  if (isCheckingAuth) {
    return (
      <div className="flex fleax-col items-center justify-center h-screen space-y-3">
        <Loader className="size-10 animate-spin" />
        <h1 className="text-gray-500 text-lg">
          Server is starting up, please wait...
        </h1>
        <p className="absolute bottom-4 left-1/2 transform -translate-x-1/2 text-sm text-gray-400">
          Creative Showcase © {new Date().getFullYear()} | Ritam Khatua
        </p>
      </div>
    );
  }

  return <AppRoutes />;
}
