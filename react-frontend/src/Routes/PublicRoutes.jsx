// External Libraries
import { Route, Routes } from "react-router-dom";

// Public Internal Modules
import About from "@/Pages/Public/About/About";
import AuthPage from "@/Pages/Public/AuthPage/AuthPage";
import Browse from "@/Pages/Public/Browse/Browse";
import Category from "@/Pages/Public/Category/Category";
import Contact from "@/Pages/Public/Contact/Contact";
import Home from "@/Pages/Public/Home/Home";
import Listing from "@/Pages/Public/Listing/Listing";
import PageNotFound from "@/Pages/Public/PageNotFound/PageNotFound";
import Search from "@/Pages/Public/Search/Search";

// Internal Authentication Modules
import AuthProvider from "@/ContextAPI/AuthProvider";
import PrivateRoute from "@/Routes/PrivateRoute";
import StaffRoute from "@/Routes/StaffRoute";
import AdminRoute from "@/Routes/AdminRoute";

// Private Internal Modules
import ListingDetails from "@/Pages/Private/ListingDetails/ListingDetails";
import Lists from "@/Pages/Private/Lists/Lists";
import Messages from "@/Pages/Private/Messages/Messages";
import MyBids from "@/Pages/Private/MyBids/MyBids";
import Orders from "@/Pages/Private/Orders/Orders";
import ProductUpload from "@/Pages/Private/ProductUpload/ProductUpload";
import Report from "@/Pages/Private/Report/Report";
import Review from "@/Pages/Private/Review/Review";
import Security from "@/Pages/Private/Security/Security";
import SellerProfile from "@/Pages/Private/SellerProfile/SellerProfile";
import UserAccount from "@/Pages/Private/UserAccount/UserAccount";
import UserProfile from "@/Pages/Private/UserProfile/UserProfile";

// Staff Internal Modules
import CustomerInquiries from "@/Pages/Staff/CustomerInquiries/CustomerInquiries";
import ListingReports from "@/Pages/Staff/ListingReports/ListingReports";
import ManageListings from "@/Pages/Staff/ManageListings/ManageListings";
import StaffAccount from "@/Pages/Staff/StaffAccount/StaffAccount";
import StaffDashboard from "@/Pages/Staff/StaffDashboard/StaffDashboard";
import StaffProfile from "@/Pages/Staff/StaffProfile/StaffProfile";

// Admin Internal Modules
import AdminAccount from "@/Pages/Admin/AdminAccount/AdminAccount";
import AdminDashboard from "@/Pages/Admin/AdminDashboard/AdminDashboard";
import AdminProfile from "@/Pages/Admin/AdminProfile/AdminProfile";
import ManageUsers from "@/Pages/Admin/ManageUsers/ManageUsers";
import SiteSettings from "@/Pages/Admin/SiteSettings/SiteSettings";
import SystemLogs from "@/Pages/Admin/SystemLogs/SystemLogs";

/**
 * PublicRoutes Component
 *
 * This component defines the routing structure for both public and private sections of the application.
 * It utilizes the `AuthProvider` context to manage the user's authentication state. The routing setup includes:
 * - Public routes that are accessible to all users.
 * - Private routes that are protected by the `PrivateRoute` component, allowing access only to authenticated users.
 * - Staff routes that are protected by the `StaffRoute` component, allowing access only to authenticated users with staff privileges.
 * - Admin routes that are protected by the `AdminRoute` component, allowing access only to authenticated users with admin privileges.
 *
 * @returns {JSX.Element} The configured routes for public and private pages.
 */
const PublicRoutes = () => {

    return (
        <AuthProvider>
            <Routes>
                {/* Public PublicRoutes */}
                <Route path="/about" element={<About />} />
                <Route path="/auth-page" element={<AuthPage />} />
                <Route path="/browse" element={<Browse />} />
                <Route path="/category" element={<Category />} />
                <Route path="/contact" element={<Contact />} />
                <Route path="/" element={<Home />} />
                <Route path="/listing" element={<Listing />} />
                <Route path="*" element={<PageNotFound />} />
                <Route path="/search" element={<Search />} />

                {/* Protected PublicRoutes for Authenticated Users */}
                <Route element={<PrivateRoute />}>
                    <Route path="/user/listings/:id" element={<ListingDetails />} />
                    <Route path="/user/lists" element={<Lists />} />
                    <Route path="/user/messages" element={<Messages />} />
                    <Route path="/user/my-bids" element={<MyBids />} />
                    <Route path="/user/orders" element={<Orders />} />
                    <Route path="/user/upload-product" element={<ProductUpload />} />
                    <Route path="/user/report" element={<Report />} />
                    <Route path="/user/review" element={<Review />} />
                    <Route path="/user/security" element={<Security />} />
                    <Route path="/user/seller-profile" element={<SellerProfile />} />
                    <Route path="/user/account" element={<UserAccount />} />
                    <Route path="/user/profile" element={<UserProfile />} />
                </Route>

                {/* Protected PublicRoutes for Staff Users */}
                <Route element={<StaffRoute />}>
                    <Route path="/staff/messages" element={<CustomerInquiries />} />
                    <Route path="/staff/reports" element={<ListingReports />} />
                    <Route path="/staff/manage-listings" element={<ManageListings />} />
                    <Route path="/staff/account" element={<StaffAccount />} />
                    <Route path="/staff/dashboard" element={<StaffDashboard />} />
                    <Route path="/staff/profile" element={<StaffProfile />} />
                </Route>

                {/* Protected PublicRoutes for Admin Users */}
                <Route element={<AdminRoute />}>
                    <Route path="/admin/account" element={<AdminAccount />} />
                    <Route path="/admin/dashboard" element={<AdminDashboard />} />
                    <Route path="/admin/profile" element={<AdminProfile />} />
                    <Route path="/admin/users" element={<ManageUsers />} />
                    <Route path="/admin/settings" element={<SiteSettings />} />
                    <Route path="/admin/logs" element={<SystemLogs />} />
                </Route>
            </Routes>
        </AuthProvider>
    )
};

export default PublicRoutes;
