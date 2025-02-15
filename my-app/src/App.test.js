import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom'; // Импортируем BrowserRouter
import App from './App';

test('renders "Добро пожаловать на сайт" on the home page', () => {
  render(
    <BrowserRouter>
      <App />
    </BrowserRouter>
  );

  const welcomeText = screen.getByText(/добро пожаловать на сайт/i);
  expect(welcomeText).toBeInTheDocument();
});