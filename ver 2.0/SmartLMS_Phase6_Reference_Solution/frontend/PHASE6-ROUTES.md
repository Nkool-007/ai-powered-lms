# Phase 6 Route Integration

Merge the Phase 6 AI route into the existing Phase 4/5 `frontend/src/App.jsx`.

Import the Instructor AI Quiz page if it is not already imported:

```jsx
import AIQuizGenerator from "./pages/instructor/AIQuizGenerator";
```

Inside the existing Instructor `ProtectedRoute`, add:

```jsx
<Route
  path="/instructor/courses/:courseId/lessons/:lessonId/ai-quiz"
  element={<AIQuizGenerator />}
/>
```

The existing Student route `/student/ai` should continue to render `AITutor`, but Phase 6 replaces the old placeholder component with the working implementation included in this package.

Add `AIIndexButton` to an owned Course management screen when you want the Instructor to rebuild the Course vector index.
