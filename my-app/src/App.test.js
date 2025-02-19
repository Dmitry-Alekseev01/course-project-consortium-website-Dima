import { render, screen } from '@testing-library/react';
import App from './App';
import { BrowserRouter } from 'react-router-dom';

// Мок для react-router-dom
jest.mock('react-router-dom', () => ({
  BrowserRouter: ({ children }) => <div>{children}</div>,
  Routes: ({ children }) => <div>{children}</div>,
  Route: ({ element }) => <div>{element}</div>,
  Navigate: () => <div>Mock Navigate</div>,
}));

test('renders "Добро пожаловать на сайт" on the home page', () => {
  render(
    <BrowserRouter>
      <App />
    </BrowserRouter>
  );

  const welcomeText = screen.getByText(/добро пожаловать на сайт/i);
  expect(welcomeText).toBeInTheDocument();
});