import AppRouter from "./Routing/AppRouter";
import { LanguageProvider } from './components/LanguageContext/LanguageContext';

function App() {
  return (
    <LanguageProvider>
    <div className="App">
      <AppRouter />
    </div>
    </LanguageProvider>
  );
}
export default App;