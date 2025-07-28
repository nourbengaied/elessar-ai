# Freelancer Transaction Classifier Frontend

A modern React frontend for the Freelancer Transaction Classifier application.

## Features

- Modern UI/UX with Tailwind CSS
- Authentication system
- Dashboard with statistics and charts
- Transaction management
- File upload with drag-and-drop
- Reports and exports
- Real-time feedback

## Tech Stack

- React 18 with TypeScript
- Tailwind CSS
- React Router
- Axios for API calls
- React Dropzone
- Recharts for charts
- React Hot Toast

## Getting Started

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm start
```

3. Build for production:
```bash
npm run build
```

## Project Structure

```
frontend/
├── src/
│   ├── components/     # Reusable components
│   ├── contexts/       # React contexts
│   ├── pages/         # Page components
│   ├── services/      # API services
│   └── App.tsx        # Main app component
```

## API Integration

The frontend communicates with the backend API at `http://localhost:8000`.

## Environment Variables

Create `.env` file:
```
REACT_APP_API_URL=http://localhost:8000
``` 