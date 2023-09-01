import Home from "./pages/Home";
import ThemeProvider from "@/theme/ThemeProvider";


function App() {
  return (
    <ThemeProvider>
      <Home />
    </ThemeProvider>
  );
}

export default App;
