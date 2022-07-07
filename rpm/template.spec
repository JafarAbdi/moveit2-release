%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/humble/.*$
%global __requires_exclude_from ^/opt/ros/humble/.*$

Name:           ros-humble-moveit-core
Version:        100.0.0
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS moveit_core package

License:        BSD
URL:            http://moveit.ros.org
Source0:        %{name}-%{version}.tar.gz

Requires:       assimp-devel
Requires:       boost-devel
Requires:       boost-python%{python3_pkgversion}-devel
Requires:       bullet-devel
Requires:       eigen3-devel
Requires:       fcl-devel
Requires:       ros-humble-angles
Requires:       ros-humble-common-interfaces
Requires:       ros-humble-eigen-stl-containers
Requires:       ros-humble-eigen3-cmake-module
Requires:       ros-humble-geometric-shapes
Requires:       ros-humble-geometry-msgs
Requires:       ros-humble-kdl-parser
Requires:       ros-humble-moveit-common
Requires:       ros-humble-moveit-msgs
Requires:       ros-humble-octomap
Requires:       ros-humble-octomap-msgs
Requires:       ros-humble-pluginlib
Requires:       ros-humble-pybind11-vendor
Requires:       ros-humble-random-numbers
Requires:       ros-humble-rclcpp
Requires:       ros-humble-ruckig
Requires:       ros-humble-sensor-msgs
Requires:       ros-humble-shape-msgs
Requires:       ros-humble-srdfdom
Requires:       ros-humble-std-msgs
Requires:       ros-humble-tf2
Requires:       ros-humble-tf2-eigen
Requires:       ros-humble-tf2-geometry-msgs
Requires:       ros-humble-trajectory-msgs
Requires:       ros-humble-urdf
Requires:       ros-humble-urdfdom
Requires:       ros-humble-urdfdom-headers
Requires:       ros-humble-visualization-msgs
Requires:       ros-humble-ros-workspace
BuildRequires:  assimp-devel
BuildRequires:  boost-devel
BuildRequires:  boost-python%{python3_pkgversion}-devel
BuildRequires:  bullet-devel
BuildRequires:  eigen3-devel
BuildRequires:  fcl-devel
BuildRequires:  pkgconfig
BuildRequires:  ros-humble-ament-cmake
BuildRequires:  ros-humble-angles
BuildRequires:  ros-humble-common-interfaces
BuildRequires:  ros-humble-eigen-stl-containers
BuildRequires:  ros-humble-eigen3-cmake-module
BuildRequires:  ros-humble-geometric-shapes
BuildRequires:  ros-humble-geometry-msgs
BuildRequires:  ros-humble-kdl-parser
BuildRequires:  ros-humble-moveit-common
BuildRequires:  ros-humble-moveit-msgs
BuildRequires:  ros-humble-octomap
BuildRequires:  ros-humble-octomap-msgs
BuildRequires:  ros-humble-pluginlib
BuildRequires:  ros-humble-pybind11-vendor
BuildRequires:  ros-humble-random-numbers
BuildRequires:  ros-humble-rclcpp
BuildRequires:  ros-humble-ruckig
BuildRequires:  ros-humble-sensor-msgs
BuildRequires:  ros-humble-shape-msgs
BuildRequires:  ros-humble-srdfdom
BuildRequires:  ros-humble-std-msgs
BuildRequires:  ros-humble-tf2
BuildRequires:  ros-humble-tf2-eigen
BuildRequires:  ros-humble-tf2-geometry-msgs
BuildRequires:  ros-humble-trajectory-msgs
BuildRequires:  ros-humble-urdf
BuildRequires:  ros-humble-urdfdom
BuildRequires:  ros-humble-urdfdom-headers
BuildRequires:  ros-humble-visualization-msgs
BuildRequires:  ros-humble-ros-workspace
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%if 0%{?with_tests}
BuildRequires:  ros-humble-ament-cmake-gmock
BuildRequires:  ros-humble-ament-cmake-gtest
BuildRequires:  ros-humble-ament-index-cpp
BuildRequires:  ros-humble-ament-lint-auto
BuildRequires:  ros-humble-ament-lint-common
BuildRequires:  ros-humble-moveit-resources-panda-moveit-config
BuildRequires:  ros-humble-moveit-resources-pr2-description
BuildRequires:  ros-humble-orocos-kdl-vendor
BuildRequires:  ros-humble-tf2-kdl
%endif

%description
Core libraries used by MoveIt

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/humble/setup.sh" ]; then . "/opt/ros/humble/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/humble" \
    -DAMENT_PREFIX_PATH="/opt/ros/humble" \
    -DCMAKE_PREFIX_PATH="/opt/ros/humble" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/humble/setup.sh" ]; then . "/opt/ros/humble/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/humble/setup.sh" ]; then . "/opt/ros/humble/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/humble

%changelog
* Thu Jul 07 2022 Henning Kayser <henningkayser@picknik.ai> - 100.0.0-1
- Autogenerated by Bloom

