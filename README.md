## Intro

This project explains how to share AVD system images (Emulator) for others to use with Android Studio.

## How to use

The [NCAR](https://github.com/nkh-lab/aosp-ncar-manifest) project is used as an example of an AOSP project.

### 1. Build SDK package and generate System Image XML file

- Build **SDK package** for you AOSP device:
```
$ . ./build/envsetup.sh
$ lunch ncar_x86-userdebug
$ make sdk
```
- Generate **System Image XML** file for hosting **SDK package** in Android Studio:
```
$ . ./vendor/nkh-lab/tools/share-avd/scripts/gen-sys-img-xml.sh
System Image XML file has been built:
/home/user1/ncar/out/host/linux-x86/sdk/ncar_x86/android-sdk_eng.user1_linux-x86.xml
```
`Note:` The default [TAG_ID](templates/sys-img-template.xml) is **android-automotive**, if you need to use a different one, then pass it to the gen script, for example:
```
$ . ./gen-sys-img-xml.sh android-tv
``` 
- Now **SDK package** and **System Image XML** file can be shared.

### 2. Add Emulator to Android Studio
- Put **SDK package** and **System Image XML** file in one folder.
- In Android Studio, select **Tools > SDK Manager**.
- Click the **SDK Update Sites** tab.
- Click **+** to add new one.
- Enter the name and path to **System Image XML** file in popup window:
```
Name: NCAR
URL: /home/user2/shared-avds/android-sdk_eng.user1_linux-x86.xml
```
- Click **OK**.
- Click **Apply** on main **SDK Manager** form.
- Switch to the **SDK Platforms** tab.
- Enable the **Show Package Details** checkbox.
- Enable **ncar emulator** under **Android API (Sv2)**.
- Click **OK**.

### 3. Create Android Virtual Device in Android Studio
- Restart Android Studio before creating an AVD.
- In Android Studio, select **Tools > Device Manager**.
- Click **Create Device**.
- Select **Automotive** from the **Category** menu list.
- Click **New Hardware Profile** or **Clone** on an existing default device and then configure the settings (`Note:` For given example **Device Type** should be set as **Android Automotive**) and click **Finish**.
- Click **Next**.
- On **x86 Images** select **ncar emulator** in **Target** row.
- Click **Finish**.
- **NCAR API 32** device should be now visible in the **Device** list.
