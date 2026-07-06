import Header from "./components/Header";
import Form93Page from "./pages/Form93";

export default function App() {
  return (
    <div className="min-h-screen bg-slate-100">
      <Header />
      <Form93Page />
      <footer className="text-center text-xs text-slate-400 py-6">
        PAN FORM AUTOMATOR &middot; GAGANGIRI MULTI SERVICES &middot; PAN CARD FORM 
      </footer>
    </div>
  );
}
