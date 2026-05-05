# Migration to Next.js and DevExtreme (DevExpress)

This plan outlines the steps to rewrite the current Node/Express/EJS frontend into a modern Next.js application using React and DevExtreme components.

## User Review Required

> [!IMPORTANT]
> The current frontend uses EJS templates. The new one will use React. I will create a new directory `front-next` for this migration to keep the original code intact until the transition is complete.

> [!NOTE]
> I will use Next.js App Router and TypeScript for better maintainability and performance.

## Proposed Changes

### [NEW] Next.js Application (`front-next`)

#### [NEW] [Project Creation]
- Initialize Next.js project with App Router and TypeScript.
- Install `devextreme`, `devextreme-react`, and `lucide-react`.

#### [NEW] [Configuration]
- Configure global styles to include DevExtreme themes (Material Blue Light or similar).
- Setup environment variables for the API URL (`http://localhost:3000/api/v1`).

#### [NEW] [Components]
- **Layout**: Navbar and Sidebar for navigation.
- **DataGrid Components**: Shared components for displaying Orders, Customers, Products, and Suppliers.
- **Form Components**: Porting EJS forms to DevExtreme React forms.

#### [NEW] [Pages]
- `/orders`: DataGrid for viewing and managing orders.
- `/orders/[id]`: Order details and item management.
- `/customers`, `/products`, `/suppliers`: Management grids for other entities.

## Verification Plan

### Automated Tests
- Build the Next.js app using `npm run build`.
- Verify page routing and component rendering using a browser tool.

### Manual Verification
- Test data loading from the backend.
- Test CRUD operations on orders and items.
- Ensure DevExtreme components (grids, buttons, forms) behave as expected.
