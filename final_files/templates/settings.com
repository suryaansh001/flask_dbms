code set<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8" />
    <meta content="width=device-width, initial-scale=1.0" name="viewport" />
    <title>Settings</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" rel="stylesheet" />
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet" />
    <style>
        body {
            font-family: 'Inter', sans-serif;
        }
    </style>
</head>

<body class="bg-gray-100">
    <!-- Layout: Sidebar + Main Content -->
    <div class="flex h-screen">
        <!-- Sidebar -->
        <div class="w-64 bg-white h-screen shadow-lg">
            <div class="p-6">
                <div class="flex items-center space-x-3">
                    <div class="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center">
                        <i class="fas fa-user-circle text-white"></i>
                    </div>
                    <span class="text-xl font-semibold">User Dashboard</span>
                </div>
            </div>
            <nav class="mt-10">
                <a href="{{ url_for('dashboard') }}" class="flex items-center p-3 text-gray-700 hover:bg-gray-200">
                    <i class="fas fa-tachometer-alt mr-3"></i>
                    <span>Dashboard</span>
                </a>
                <a href="{{ url_for('placement_records') }}" class="flex items-center p-3 text-gray-700 hover:bg-gray-200">
                    <i class="fas fa-check-circle mr-3"></i>
                    <span>Placement Records</span>
                </a>
                <a href="{{ url_for('apply') }}" class="flex items-center p-3 text-gray-700 hover:bg-gray-200">
                    <i class="fas fa-file-alt mr-3"></i>
                    <span>Apply for Jobs</span>
                </a>
                <a href="{{ url_for('settings') }}" class="flex items-center p-3 text-gray-700 hover:bg-gray-200">
                    <i class="fas fa-cogs mr-3"></i>
                    <span>Settings</span>
                </a>
                <a href="{{ url_for('logout') }}" class="flex items-center p-3 text-gray-700 hover:bg-gray-200">
                    <i class="fas fa-sign-out-alt mr-3"></i>
                    <span>Logout</span>
                </a>
            </nav>
        </div>

        <!-- Main Content -->
        <div class="flex flex-col flex-grow p-6">
            <h2 class="text-2xl font-semibold mb-6">Account Settings</h2>

            <!-- Settings Form -->
            <div class="bg-white p-6 rounded-lg shadow-md">
                <form action="{{ url_for('update_settings') }}" method="POST">
                    <div class="mb-4">
                        <label for="roll_number" class="block text-sm font-medium text-gray-700">Roll Number</label>
                        <input type="text" id="roll_number" name="roll_number" class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500" value="{{ user.roll_number }}" required>
                    </div>

                    <div class="mb-4">
                        <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
                        <input type="email" id="email" name="email" class="mt-1 block w-full px-4 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500" value="{{ user.email }}" required>
                    </div>

                    <div class="mb-6">
                        <button type="submit" class="w-full bg-blue-500 text-white px-4 py-2 rounded-full hover:bg-blue-600">
                            Save Changes
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>

</body>

</html>
